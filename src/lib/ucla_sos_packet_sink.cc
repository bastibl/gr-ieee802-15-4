/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

/*
 * ucla_sos_packet_sink.cc has been derived from gr_packet_sink.cc
 *
 * Modified by: Thomas Schmid
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <ucla_sos_packet_sink.h>
#include <gr_io_signature.h>
#include <cstdio>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdexcept>
#include <cstring>
#include <gr_count_bits.h>

#define VERBOSE 0

static const int DEFAULT_THRESHOLD = 0;  // detect access code with up to DEFAULT_THRESHOLD bits wrong

inline void
ucla_sos_packet_sink::enter_search()
{
  if (VERBOSE)
    fprintf(stderr, "@ enter_search\n");

  d_state = STATE_SYNC_SEARCH;
  d_shift_reg = 0;
}
    
inline void
ucla_sos_packet_sink::enter_have_sync()
{
  if (VERBOSE)
    fprintf(stderr, "@ enter_have_sync\n");

  d_state = STATE_HAVE_SYNC;
  d_packetlen_cnt = 0;
  d_packet_byte = 0;
  d_packet_byte_index = 0;
}

inline void
ucla_sos_packet_sink::enter_have_header(int payload_len)
{
  if (VERBOSE)
    fprintf(stderr, "@ enter_have_header (payload_len = %d)\n", payload_len);
  
  d_state = STATE_HAVE_HEADER;
  d_packetlen  = payload_len;
  d_payload_cnt = 0;
  d_packet_byte = 0;
  d_packet_byte_manchester = 0;
  d_packet_byte_index = 0;
}

ucla_sos_packet_sink_sptr
ucla_make_sos_packet_sink (const std::vector<unsigned char>& sync_vector,
			   gr_msg_queue_sptr target_queue, 
			   int threshold)
{
  return ucla_sos_packet_sink_sptr (new ucla_sos_packet_sink (sync_vector, target_queue, threshold));
}


ucla_sos_packet_sink::ucla_sos_packet_sink (const std::vector<unsigned char>& sync_vector,
					    gr_msg_queue_sptr target_queue, int threshold)
  : gr_sync_block ("sos_packet_sink",
		   gr_make_io_signature (1, 1, sizeof(float)),
		   gr_make_io_signature (0, 0, 0)),
    d_target_queue(target_queue), 
    d_threshold(threshold == -1 ? DEFAULT_THRESHOLD : threshold),
    d_manchester  (1)
{
  d_sync_vector = 0;
  for(int i=0;i<8;i++){
    d_sync_vector <<= 8;
    d_sync_vector |= sync_vector[i];
  }
  if ( VERBOSE )
    fprintf(stderr, "syncvec: %llx\n", d_sync_vector),fflush(stderr);

  enter_search();
}

ucla_sos_packet_sink::~ucla_sos_packet_sink ()
{
}

int

ucla_sos_packet_sink::work (int noutput_items,
		      gr_vector_const_void_star &input_items,
		      gr_vector_void_star &output_items)
{
  float *inbuf = (float *) input_items[0];
  int count=0;
  
  if (VERBOSE)
    fprintf(stderr,">>> Entering state machine\n"),fflush(stderr);

  while (count<noutput_items) {
    switch(d_state) {
      
    case STATE_SYNC_SEARCH:    // Look for sync vector
      if (VERBOSE)
	fprintf(stderr,"SYNC Search, noutput=%d syncvec=%llx\n",noutput_items, d_sync_vector),fflush(stderr);

      while (count < noutput_items) {

	if(slice(inbuf[count++]))
	  d_shift_reg = (d_shift_reg << 1) | 1;
	else
	  d_shift_reg = d_shift_reg << 1;

	//if (VERBOSE)
	//  fprintf(stderr,"d_shift=%llx sync_vec=%llx\n",d_shift_reg, d_sync_vector),fflush(stderr);	

	// Compute popcnt of putative sync vector
	if(gr_count_bits64 (d_shift_reg ^ d_sync_vector) <= d_threshold) {
	  // Found it, set up for header decode
	  enter_have_sync();
	  break;
	}
      }
      break;

    case STATE_HAVE_SYNC:
      if (VERBOSE)
	fprintf(stderr,"Header Search bitcnt=%d, header=0x%08x\n", d_headerbitlen_cnt, d_header),
	  fflush(stderr);

      while (count < noutput_items) {		// Shift bits one at a time into header
	if(slice(inbuf[count++]))
	  d_packet_byte = (d_packet_byte << 1) | 1;
	else
	  d_packet_byte = d_packet_byte << 1;

	

	if (d_packet_byte_index++ == 7) {

	  if (d_manchester) {
	    if (d_packet_byte_manchester == 0){
	      d_packet_byte_manchester = d_packet_byte;
	      d_packet_byte = 0;
	      d_packet_byte_index = 0;
	      continue;
	    } else {
	      // ok, second manchester byte received, now put them together to one byte
	      //fprintf(stderr, "b1: 0x%x b2: 0x%x ", d_packet_byte_manchester, d_packet_byte);
	      d_packet_byte = manchester_decode(d_packet_byte_manchester, d_packet_byte);
	      d_packet_byte_manchester = 0;
	    }
	  } 

	  d_packet[d_packetlen_cnt++] = d_packet_byte;
	  d_packet_byte_index = 0;
	  if (VERBOSE)
	    fprintf(stderr, "byte: 0x%x ", d_packet_byte), fflush(stderr);
	}
	if (d_packetlen_cnt == MSG_LEN_POS) {

	  if (VERBOSE)
	    fprintf(stderr, "\ngot msg len: 0x%08x\n", d_packet_byte);

	  // we have the msg length, rest of the message is payload
	  if (header_ok()){
	    int payload_len = d_packet_byte;
	    if (payload_len <= MAX_PKT_LEN)		// reasonable?
	      enter_have_header(payload_len);		// yes.
	    else
	      enter_search();				// no.
	  }
	  else
	    enter_search();				// no.
	  break;			// we're in a new state
	}
      }
      break;
      
    case STATE_HAVE_HEADER:
      if (VERBOSE)
	fprintf(stderr,"Packet Build count=%d, noutput_items=%d\n", count, noutput_items),fflush(stderr);

      while (count < noutput_items) {   // shift bits into bytes of packet one at a time
	if(slice(inbuf[count++]))
	  d_packet_byte = (d_packet_byte << 1) | 1;
	else
	  d_packet_byte = d_packet_byte << 1;

	//fprintf(stderr, "packetcnt: %d, payloadcnt: %d, payload 0x%x, d_packet_byte_index: %d\n", d_packetlen_cnt, d_payload_cnt, d_packet_byte, d_packet_byte_index);

	if (d_packet_byte_index++ == 7) {	  	// byte is full so move to next byte
	  if (d_manchester) {
	    if (d_packet_byte_manchester == 0){
	      d_packet_byte_manchester = d_packet_byte;
	      d_packet_byte = 0;
	      d_packet_byte_index = 0;
	      continue;
	    } else {
	      // ok, second manchester byte received, now put them together to one byte
	      //fprintf(stderr, "b1: 0x%x b2: 0x%x ", d_packet_byte_manchester, d_packet_byte);
	      d_packet_byte = manchester_decode(d_packet_byte_manchester, d_packet_byte);
	      d_packet_byte_manchester = 0;
	    }
	  } 
	  d_packet[d_packetlen_cnt++] = d_packet_byte;
	  d_payload_cnt++;
	  d_packet_byte_index = 0;

	  if (d_payload_cnt >= d_packetlen+2){	// packet is filled, including 16 bit CRC. might do check later in here

	    // build a message
	    gr_message_sptr msg = gr_make_message(0, 0, 0, d_packetlen_cnt);  	    
	    memcpy(msg->msg(), d_packet, d_packetlen_cnt);

	    d_target_queue->insert_tail(msg);		// send it
	    msg.reset();  				// free it up
	    if(VERBOSE)
	      fprintf(stderr, "Adding message of size %d to queue\n", d_packetlen_cnt);
	    enter_search();
	    break;
	  }
	}
      }
      break;

    default:
      assert(0);

    } // switch

  }   // while

  return noutput_items;
}
  
