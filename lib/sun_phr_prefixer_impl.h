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

#ifndef INCLUDED_IEEE802_15_4_SUN_PHR_PREFIXER_IMPL_H
#define INCLUDED_IEEE802_15_4_SUN_PHR_PREFIXER_IMPL_H

#include <ieee802_15_4/sun_phr_prefixer.h>

namespace gr {
  namespace ieee802_15_4 {

    class sun_phr_prefixer_impl : public sun_phr_prefixer
    {
     private:
      const static int MAX_PREAMBLE_LEN = 8;
      const static int MAX_SFD_LEN = 4;
      const static int MAX_PHR_LEN = 8;
      const static int MAX_PSDU_LEN = 2048; // Includes CRC, FCS, or MFR
      const static int MAX_PPDU_LEN = MAX_PREAMBLE_LEN + MAX_SFD_LEN + MAX_PHR_LEN + MAX_PSDU_LEN;
      const static int MAX_FCS_LEN = 4; // Same as MFR

      unsigned char* d_buf;
      void prefix_phr(pmt::pmt_t msg);

     public:
      sun_phr_prefixer_impl(bool fcs, bool dw);
      ~sun_phr_prefixer_impl();
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_SUN_PHR_PREFIXER_IMPL_H */

