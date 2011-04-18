/* -*- c++ -*- */
/*
 * Copyright 2005 Free Software Foundation, Inc.
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

#ifndef INCLUDED_UCLA_SOS_PACKET_SINK_H
#define INCLUDED_UCLA_SOS_PACKET_SINK_H

#include <gr_sync_block.h>
#include <gr_msg_queue.h>

class ucla_sos_packet_sink;
typedef boost::shared_ptr<ucla_sos_packet_sink> ucla_sos_packet_sink_sptr;

ucla_sos_packet_sink_sptr 
ucla_make_sos_packet_sink (const std::vector<unsigned char>& sync_vector,
			   gr_msg_queue_sptr target_queue,
			   int threshold = -1	                // -1 -> use default
			   );
/*!
 * \brief process received  bits looking for packet sync, header, and process bits into packet
 * \ingroup sink
 */
class ucla_sos_packet_sink : public gr_sync_block
{
  friend ucla_sos_packet_sink_sptr 
  ucla_make_sos_packet_sink (const std::vector<unsigned char>& sync_vector,
			     gr_msg_queue_sptr target_queue,
			     int threshold);

private:
  enum state_t {STATE_SYNC_SEARCH, STATE_HAVE_SYNC, STATE_HAVE_HEADER};

  static const int MSG_LEN_POS   = 8+1;         // 8 byte sos header, 1 byte AM type
  static const int MAX_PKT_LEN    = 128 - MSG_LEN_POS - 1; // remove header and CRC

  gr_msg_queue_sptr  d_target_queue;		// where to send the packet when received
  unsigned long long d_sync_vector;		// access code to locate start of packet
  unsigned int	     d_threshold;		// how many bits may be wrong in sync vector
  unsigned char      d_manchester;              // do we use manchester encoding or not

  state_t            d_state;

  unsigned long long d_shift_reg;		// used to look for sync_vector

  unsigned int       d_header;			// header bits
  int		     d_headerbitlen_cnt;	// how many so far

  unsigned char      d_packet[MAX_PKT_LEN];	// assembled payload
  unsigned char	     d_packet_byte;		// byte being assembled
  unsigned char      d_packet_byte_manchester;  // byte which is needed for manchester encoding
  int		     d_packet_byte_index;	// which bit of d_packet_byte we're working on
  int 		     d_packetlen;		// length of packet
  int		     d_packetlen_cnt;		// how many so far
  int		     d_payload_cnt;		// how many bytes in payload
  
protected:
  ucla_sos_packet_sink(const std::vector<unsigned char>& sync_vector, 
		       gr_msg_queue_sptr target_queue,
		       int threshold);
  
  void enter_search();
  void enter_have_sync();
  void enter_have_header(int payload_len);
  
  int slice(float x) { return x > 0 ? 1 : 0; }
  
  bool header_ok()
  {
    // might do some checks on the header later...
    return 1;
  }

  unsigned char manchester_decode(unsigned char b1, unsigned char b2){
    unsigned char t, b;
    int errors = 0;

    for (unsigned char i = 0; i < 8; i += 2){
      t = (b1 >> (6 - i)) & 0x3;
      if ( t == 1 ){
	b = (b << 1) | 0;
      } else if ( t == 2 ){
	b = (b << 1) | 1;
      } else {
	// mistake in manchester encoding encode as 0
	b = (b << 1) | 0;
	errors += 1;
      }
    }

    for (unsigned char i = 0; i < 8; i += 2){
      t = (b2 >> (6 - i)) & 0x3;
      if ( t == 1 ){
	b = (b << 1) | 0;
      } else if ( t == 2 ){
	b = (b << 1) | 1;
      } else {
	// mistake in manchester encoding encode as 0
	b = (b << 1) | 0;
	errors += 1;
      }
    }
    return b;
  }

  
  
public:
  ~ucla_sos_packet_sink();

  int work(int noutput_items,
	   gr_vector_const_void_star &input_items,
	   gr_vector_void_star &output_items);


  //! return true if we detect carrier
  bool carrier_sensed() const
  {
    return d_state != STATE_SYNC_SEARCH;
  }

};

#endif /* INCLUDED_GR_PACKET_SINK_H */
