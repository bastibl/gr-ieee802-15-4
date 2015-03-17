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

#ifndef INCLUDED_IEEE802_15_4_DEINTERLEAVER_FF_IMPL_H
#define INCLUDED_IEEE802_15_4_DEINTERLEAVER_FF_IMPL_H

#include <ieee802_15_4/deinterleaver_ff.h>

namespace gr {
  namespace ieee802_15_4 {

    class deinterleaver_ff_impl : public deinterleaver_ff
    {
     private:
      std::vector<int> d_intlv_seq;
      int d_len_intlv_seq;
      bool d_forward;

     public:
      deinterleaver_ff_impl(std::vector<int> intlv_seq);
      ~deinterleaver_ff_impl();

      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_DEINTERLEAVER_FF_IMPL_H */

