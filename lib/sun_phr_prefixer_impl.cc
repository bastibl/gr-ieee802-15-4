/* -*- c++ -*- */
/* 
 * Copyright 2015 Felix Wunsch, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT) <wunsch.felix@googlemail.com>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <gnuradio/block_detail.h>
#include "sun_phr_prefixer_impl.h"

namespace gr {
  namespace ieee802_15_4 {

    sun_phr_prefixer::sptr
    sun_phr_prefixer::make(bool fcs, bool dw)
    {
      return gnuradio::get_initial_sptr
        (new sun_phr_prefixer_impl(fcs,dw));
    }

    /*
     * The private constructor
     */
    sun_phr_prefixer_impl::sun_phr_prefixer_impl(bool fcs, bool dw)
      : gr::block("sun_phr_prefixer",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
      // Alloc buffer with PHR bits 
      d_buf = new unsigned char[MAX_PSDU_LEN + MAX_PHR_LEN];
      d_buf[0] = (fcs ? 1<<3 : 0) | (dw ? 1<<4 : 0);

      // define message ports
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"), boost::bind(&sun_phr_prefixer_impl::prefix_phr, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    sun_phr_prefixer_impl::~sun_phr_prefixer_impl()
    {
      delete[] d_buf;
    }

    void
    sun_phr_prefixer_impl::prefix_phr(pmt::pmt_t msg)
    {
      if(pmt::is_eof_object(msg)) 
      {
        message_port_pub(pmt::mp("out"), pmt::PMT_EOF);
        detail().get()->set_done(true);
        return;
      }      

      if(!pmt::is_pair(msg))
        throw std::runtime_error("Input PMT is not of type pair");

      pmt::pmt_t blob = pmt::cdr(msg);
      size_t data_len = pmt::blob_length(blob);
      if(data_len > MAX_PSDU_LEN) {
        throw std::runtime_error("Payload length exceeds MAX_PSDU_LEN" );
      }

      // Reverse bits of length
      unsigned int v = data_len;
      unsigned int r = v;
      int s = 10; // frame length in bits - 1 because of extra shift at end

      for (v >>= 1; v; v >>= 1) {   
        r <<= 1;
        r |= v & 1;
        s--;
      }

      r <<= s; // shift if v's highest bits are zero

      // Put length in PHR
      unsigned int i = 0;
      d_buf[i++] |= (r & 0b00000000111)<<5;
      d_buf[i++] =  (r & 0b11111111000)>>3;

      unsigned char* blob_ptr = (unsigned char*) pmt::blob_data(blob);
      memcpy(d_buf+i, blob_ptr, data_len);
      pmt::pmt_t packet = pmt::make_blob(&d_buf[0], data_len+i);
      message_port_pub(pmt::mp("out"), pmt::cons(pmt::PMT_NIL, packet));
    }
  } /* namespace ieee802_15_4 */
} /* namespace gr */

