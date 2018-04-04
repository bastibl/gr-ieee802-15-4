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
#include "pn9_whitener_impl.h"

namespace gr {
  namespace ieee802_15_4 {

    pn9_whitener::sptr
    pn9_whitener::make(uint16_t seed)
    {
      return gnuradio::get_initial_sptr
        (new pn9_whitener_impl(seed));
    }

    /*
     * The private constructor
     */
    pn9_whitener_impl::pn9_whitener_impl(uint16_t seed)
      : gr::block("pn9_whitener",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
      uint16_t pn = seed;
      d_pn9 = new unsigned char[PN9_LEN]; // Size of array that holds entire PN9 sequence

      // Compute and save PN9 pattern for faster signal processing
      for (int i = 0; i < PN9_LEN ; i++)
      {
        for (int j = 0; j < 8; j++) // iterate through bits in byte
        {
          if ( !!(pn & (1<<12)) ^ !!(pn & (1<<7)) )
          {
            pn = (pn >> 1) | 1<<15;
          } else {
            pn = (pn >> 1);
          }
        }

        d_pn9[i] = (pn & 0xFF00)>>8;
        //std::cout << std::hex << (int)d_pn9[i] << '\n';
      }

      // define message ports
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"), boost::bind(&pn9_whitener_impl::pn9_whiten, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    pn9_whitener_impl::~pn9_whitener_impl()
    {
      delete[] d_pn9;
    }

    void
    pn9_whitener_impl::pn9_whiten(pmt::pmt_t msg)
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
        throw std::runtime_error("Payload length exceeds the maximum: " );
      }

      unsigned char* blob_ptr = (unsigned char*) pmt::blob_data(blob);

      // Whiten the blob in situ
      for (int i = 0; i < data_len; i++) {
        blob_ptr[i] ^= d_pn9[i%PN9_LEN];
      }

      // Pass it on
      pmt::pmt_t packet = pmt::make_blob(&blob_ptr[0], data_len);
      message_port_pub(pmt::mp("out"), pmt::cons(pmt::PMT_NIL, packet));
    }
  } /* namespace ieee802_15_4 */
} /* namespace gr */

