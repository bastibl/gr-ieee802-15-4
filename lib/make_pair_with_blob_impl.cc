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
#include "make_pair_with_blob_impl.h"
#include <gnuradio/block_detail.h>

namespace gr {
  namespace ieee802_15_4 {

    make_pair_with_blob::sptr
    make_pair_with_blob::make(std::vector<unsigned char> vec)
    {
      return gnuradio::get_initial_sptr
        (new make_pair_with_blob_impl(vec));
    }

    /*
     * The private constructor
     */
    make_pair_with_blob_impl::make_pair_with_blob_impl(std::vector<unsigned char> vec)
      : gr::block("make_pair_with_blob",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0)),
      d_vec(vec)
    {
      // input messages only work as trigger
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"), boost::bind(&make_pair_with_blob_impl::send_msg, this, _1));
      
    }

    /*
     * Our virtual destructor.
     */
    make_pair_with_blob_impl::~make_pair_with_blob_impl()
    {
    }

    void
    make_pair_with_blob_impl::send_msg(pmt::pmt_t msg)
    {
      if(pmt::is_eof_object(msg)) 
      {
        message_port_pub(pmt::mp("out"), pmt::PMT_EOF);
        detail().get()->set_done(true);
        return;
      }

      if(!pmt::is_pair(msg))
        throw std::runtime_error("Input PMT is not of type pair");

      pmt::pmt_t blob = pmt::make_blob(&d_vec[0], d_vec.size());
      message_port_pub(pmt::mp("out"), pmt::cons(pmt::PMT_NIL, blob));
    }
  } /* namespace ieee802_15_4 */
} /* namespace gr */

