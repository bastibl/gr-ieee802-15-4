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

#ifndef INCLUDED_IEEE802_15_4_DQCSK_MAPPER_FC_IMPL_H
#define INCLUDED_IEEE802_15_4_DQCSK_MAPPER_FC_IMPL_H

#include <ieee802_15_4/dqcsk_mapper_fc.h>

namespace gr {
  namespace ieee802_15_4 {

    class dqcsk_mapper_fc_impl : public dqcsk_mapper_fc
    {
     private:
      std::vector<gr_complex> d_chirp_seq;
      std::vector<gr_complex> d_time_gap_1;
      std::vector<gr_complex> d_time_gap_2;
      int d_len_subchirp;
      int d_num_subchirps;
      int d_chirp_seq_ctr;
      int d_subchirp_ctr;
      int d_nsym_frame;
      int d_sym_ctr;
      int max_len_timegap;

      void reset();

     public:
      dqcsk_mapper_fc_impl(std::vector<gr_complex> chirp_seq, std::vector<gr_complex> time_gap_1, std::vector<gr_complex> time_gap_2, int len_subchirp, int num_subchirps, int nsym_frame);
      ~dqcsk_mapper_fc_impl();

      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_DQCSK_MAPPER_FC_IMPL_H */

