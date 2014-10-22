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
#include "compare_blobs_impl.h"

namespace gr {
  namespace ieee802_15_4 {

    compare_blobs::sptr
    compare_blobs::make(bool packet_error_mode)
    {
      return gnuradio::get_initial_sptr
        (new compare_blobs_impl(packet_error_mode));
    }

    /*
     * The private constructor
     */
    compare_blobs_impl::compare_blobs_impl(bool packet_error_mode)
      : gr::block("compare_blobs",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0)),
      d_packet_error_mode(packet_error_mode),
      d_num_bits_compared(0),
      d_num_errors_found(0)
    {
      if(d_packet_error_mode)
        throw std::runtime_error("Packet error mode not implemented yet!");

      d_stored_ref.clear();
      d_stored_test.clear();

      message_port_register_in(pmt::mp("ref"));
      set_msg_handler(pmt::mp("ref"), boost::bind(&compare_blobs_impl::store_ref, this, _1));
      message_port_register_in(pmt::mp("test"));
      set_msg_handler(pmt::mp("test"), boost::bind(&compare_blobs_impl::store_test, this, _1));     
    }

    /*
     * Our virtual destructor.
     */
    compare_blobs_impl::~compare_blobs_impl()
    {}

    void
    compare_blobs_impl::store_ref(pmt::pmt_t msg)
    {
      if(!pmt::is_pair(msg))
        throw std::runtime_error("Input message type must be pair");

      d_stored_ref.push_back(pmt::cdr(msg));
      if(d_stored_test.size() > 0)
        compare_bits();
    }

    void
    compare_blobs_impl::store_test(pmt::pmt_t msg)
    {
      if(!pmt::is_pair(msg))
        throw std::runtime_error("Input message type must be pair");

      d_stored_test.push_back(pmt::cdr(msg));
      if(d_stored_ref.size() > 0)
        compare_bits();
    }

    void
    compare_blobs_impl::compare_bits()
    {
      if(pmt::blob_length(d_stored_ref[0]) != pmt::blob_length(d_stored_test[0]))
        throw std::runtime_error("Blobs must have same size");

      int num_bytes = pmt::blob_length(d_stored_ref[0]);
      unsigned char* ref_ptr = (unsigned char*) pmt::blob_data(d_stored_ref[0]);
      unsigned char* test_ptr = (unsigned char*) pmt::blob_data(d_stored_test[0]);

      unsigned char bit_ref, bit_test;
      for(int i=0; i<num_bytes; i++)
      {
        // std::cout << "i: " << i << " --> ref=" << int(ref_ptr[i]) << ", test=" << int(test_ptr[i]) << std::endl;
        for(int n=0; n<8; n++)
        {
          bit_ref = (ref_ptr[i] >> n) & 0x01;
          bit_test = (test_ptr[i] >> n) & 0x01;
          // std::cout << "compare bit #" << n << ": " << int(bit_ref) << " <--> " << int(bit_test) << std::endl;
          if(bit_ref != bit_test)
            d_num_errors_found++;
        }
      }
      d_num_bits_compared += num_bytes*8;

      d_stored_ref.erase(d_stored_ref.begin());
      d_stored_test.erase(d_stored_test.begin());
    }
  } /* namespace ieee802_15_4 */
} /* namespace gr */

