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

#ifndef INCLUDED_IEEE802_15_4_FRAGMENTATION_IMPL_H
#define INCLUDED_IEEE802_15_4_FRAGMENTATION_IMPL_H

#include <ieee802_15_4/fragmentation.h>

namespace gr {
  namespace ieee802_15_4 {

    class fragmentation_impl : public fragmentation
    {
     private:
      int d_nbytes;
      std::vector<char> d_buf;
      void create_packets(pmt::pmt_t msg);

     public:
      fragmentation_impl(int nbytes);
      ~fragmentation_impl();
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_FRAGMENTATION_IMPL_H */

