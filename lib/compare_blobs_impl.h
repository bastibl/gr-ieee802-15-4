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

#ifndef INCLUDED_IEEE802_15_4_COMPARE_BLOBS_IMPL_H
#define INCLUDED_IEEE802_15_4_COMPARE_BLOBS_IMPL_H

#include <ieee802_15_4/compare_blobs.h>

namespace gr {
  namespace ieee802_15_4 {

    class compare_blobs_impl : public compare_blobs
    {
     private:
      std::vector<pmt::pmt_t> d_stored_ref;
      std::vector<pmt::pmt_t> d_stored_test;
      bool d_packet_error_mode;
      int d_num_bits_compared;
      int d_num_errors_found;

     public:
      compare_blobs_impl(bool packet_error_mode);
      ~compare_blobs_impl();

      void store_test(pmt::pmt_t msg);
      void store_ref(pmt::pmt_t msg);
      void compare_bits();

      int get_bits_compared(){ return d_num_bits_compared; }
      int get_errors_found(){ return d_num_errors_found; }
      float get_ber(){ return float(d_num_errors_found)/d_num_bits_compared; }
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_COMPARE_BLOBS_IMPL_H */

