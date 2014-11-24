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

#ifndef INCLUDED_IEEE802_15_4_RAYLEIGH_MULTIPATH_CC_IMPL_H
#define INCLUDED_IEEE802_15_4_RAYLEIGH_MULTIPATH_CC_IMPL_H

#include <ieee802_15_4/rayleigh_multipath_cc.h>
#include <random>

namespace gr {
  namespace ieee802_15_4 {

    class rayleigh_multipath_cc_impl : public rayleigh_multipath_cc
    {
     private:
      std::vector<float> d_pdp; // power delay profile
      int d_len_pdp;
      int d_coh_time_samps; // coherence time in samples
      int d_samp_ctr; // counts samples to determine the time for the channel reset
      std::vector<gr_complex> d_taps; // the generated filter taps
      void generate_taps();
      std::default_random_engine d_gen;
      std::normal_distribution<float> d_rand; // random number generator

     public:
      rayleigh_multipath_cc_impl(std::vector<float> pdp, int coherence_time_samps);
      ~rayleigh_multipath_cc_impl();

      std::vector<gr_complex> taps(){ return d_taps; }

      // Where all the action really happens
      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_RAYLEIGH_MULTIPATH_CC_IMPL_H */

