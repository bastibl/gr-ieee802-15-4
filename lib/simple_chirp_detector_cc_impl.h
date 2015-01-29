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

#ifndef INCLUDED_IEEE802_15_4_SIMPLE_CHIRP_DETECTOR_CC_IMPL_H
#define INCLUDED_IEEE802_15_4_SIMPLE_CHIRP_DETECTOR_CC_IMPL_H

#include <ieee802_15_4/simple_chirp_detector_cc.h>

namespace gr {
  namespace ieee802_15_4 {

    class simple_chirp_detector_cc_impl : public simple_chirp_detector_cc
    {
     private:
      std::vector<gr_complex> d_chirp_seq;
      int d_time_gap_1;
      int d_time_gap_2;
      int d_len_subchirp;
      float d_threshold;
      gr_complex d_e_subchirp; // actually is a float, but needs to be complex for the / operator to be defined
      gr_complex correlate_with_subchirp(const gr_complex* buf, int chirp_number); // normalized correlation
      bool corr_over_threshold(gr_complex corrval);

     public:
      #define dout false && std::cout // turn false to true to enable debug output

      simple_chirp_detector_cc_impl(std::vector<gr_complex> chirp_seq, int time_gap_1, int time_gap_2, int len_subchirp, float threshold);
      ~simple_chirp_detector_cc_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_SIMPLE_CHIRP_DETECTOR_CC_IMPL_H */

