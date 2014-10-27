/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
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
#include "fragmentation_impl.h"

namespace gr {
  namespace ieee802_15_4 {

    fragmentation::sptr
    fragmentation::make(int nbytes)
    {
      return gnuradio::get_initial_sptr
        (new fragmentation_impl(nbytes));
    }

    /*
     * The private constructor
     */
    fragmentation_impl::fragmentation_impl(int nbytes)
      : gr::block("fragmentation",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0)),
      d_nbytes(nbytes)
    {
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"), boost::bind(&fragmentation_impl::create_packets, this, _1));
      
      d_buf.clear();
    }

    /*
     * Our virtual destructor.
     */
    fragmentation_impl::~fragmentation_impl()
    {
    }

    void
    fragmentation_impl::create_packets(pmt::pmt_t msg)
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
      char* blob_ptr = (char*) pmt::blob_data(blob);
      for(int i=0; i<data_len; i++)
      {
        if(d_buf.size() < d_nbytes)
        {
          d_buf.push_back(blob_ptr[i]);
        }
        if(d_buf.size() == d_nbytes)
        {
          pmt::pmt_t packet = pmt::make_blob(&d_buf[0], d_nbytes);
          message_port_pub(pmt::mp("out"), pmt::cons(pmt::PMT_NIL, packet));
          d_buf.clear();          
        }

      }
    }
  } /* namespace ieee802_15_4 */
} /* namespace gr */

