/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
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

#ifndef INCLUDED_IEEE802_15_4_PREAMBLE_DETECTION_CC_IMPL_H
#define INCLUDED_IEEE802_15_4_PREAMBLE_DETECTION_CC_IMPL_H

#include <ieee802_15_4/preamble_detection_cc.h>
#include <boost/circular_buffer.hpp>

namespace gr {
  namespace ieee802_15_4 {

    class preamble_detection_cc_impl : public preamble_detection_cc
    {
     private:
      int d_len_preamble;
      gr_complex d_preamble_sym;
      bool d_preamble_detected;
      boost::circular_buffer<gr_complex> d_buf;
      float d_phi_off;
      int num_returnable_items(int in_avail, int out_avail, int nread, int nwritten){ return std::min(in_avail - nread, out_avail - nwritten); }
      #define dout false && std::cout // turn false to true to enable debug output

     public:
      preamble_detection_cc_impl(int len_preamble, gr_complex preamble_sym);
      ~preamble_detection_cc_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_PREAMBLE_DETECTION_CC_IMPL_H */

