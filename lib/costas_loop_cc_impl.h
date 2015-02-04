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

#ifndef INCLUDED_IEEE802_15_4_COSTAS_LOOP_CC_IMPL_H
#define INCLUDED_IEEE802_15_4_COSTAS_LOOP_CC_IMPL_H

#include <ieee802_15_4/costas_loop_cc.h>

namespace gr {
  namespace ieee802_15_4 {

    class costas_loop_cc_impl : public costas_loop_cc
    {
     private:
      static const int NO_INIT_PHASE = -1;
      static const int FIRST_RUN = -1;
      std::vector<gr_complex> d_const;
      int d_M;
      int d_initial_index;
      int d_last_index;
      float* d_diff;
      float d_phase_offset;
      int get_nearest_index(gr_complex p);
      void reset();

     public:
      #define dout false && std::cout // turn false to true to enable debug output
      costas_loop_cc_impl(std::vector<gr_complex> constellation_points, int initial_index);
      ~costas_loop_cc_impl();

      // Where all the action really happens
      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_COSTAS_LOOP_CC_IMPL_H */

