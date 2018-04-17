/* -*- c++ -*- */
/* 
 * Copyright 2018 Fred Fierling, Spukhafte Systems Limited
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
#include "pdu_wrapper_impl.h"

namespace gr {
  namespace ieee802_15_4 {

    pdu_wrapper::sptr
    pdu_wrapper::make(std::vector<unsigned char> prefix, std::vector<unsigned char> suffix)
    {
      return gnuradio::get_initial_sptr
        (new pdu_wrapper_impl(prefix, suffix));
    }

    /*
     * The private constructor
     */
    pdu_wrapper_impl::pdu_wrapper_impl(std::vector<unsigned char> prefix,
      std::vector<unsigned char> suffix)
      : gr::block("pdu_wrapper",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0)),
              d_prefix_size(sizeof(unsigned char)*prefix.size()),
              d_suffix_size(sizeof(unsigned char)*suffix.size())
    {
      // check input vector and prepare the buffer with for the prefix
      if(d_prefix_size > MAX_PHR_LEN) {
        throw std::runtime_error(str(boost::format("Prefix size must be less than %d bytes")
          % static_cast<int>(MAX_PHR_LEN) )); 
      }

      // check input vector and prepare the buffer with for the suffix
      if(d_suffix_size > MAX_PHR_LEN) {
        throw std::runtime_error(str(boost::format("Suffix size must be less than %d bytes")
          % static_cast<int>(MAX_PHR_LEN) )); 
      }

      // Start by copying prefix into buffer
      d_buf = new unsigned char[MAX_PPDU_LEN];
      memcpy(d_buf, &prefix[0], sizeof(unsigned char)*d_prefix_size);

      // Copy suffix
      d_suffix = new unsigned char[MAX_PHR_LEN];
      memcpy(d_suffix, &suffix[0], sizeof(unsigned char)*d_suffix_size);

      // define message ports
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"), boost::bind(&pdu_wrapper_impl::wrapper, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    pdu_wrapper_impl::~pdu_wrapper_impl()
    {
      delete[] d_buf;
      delete[] d_suffix;
    }

    void
    pdu_wrapper_impl::wrapper(pmt::pmt_t msg)
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
      if(data_len > GRPW_MAX_PSDU_LEN) {
        throw std::runtime_error(str(boost::format("Payload length exceeds the maximum: %d bytes")
          % GRPW_MAX_PSDU_LEN ));
      }

      unsigned char* blob_ptr = (unsigned char*) pmt::blob_data(blob);
      memcpy(&d_buf[d_prefix_size], blob_ptr, data_len);

      memcpy(&d_buf[d_prefix_size + data_len], d_suffix, d_suffix_size);

      pmt::pmt_t packet = pmt::make_blob(&d_buf[0], d_prefix_size+data_len+d_suffix_size);
      message_port_pub(pmt::mp("out"), pmt::cons(pmt::PMT_NIL, packet));
    }
  } /* namespace ieee802_15_4 */
} /* namespace gr */

