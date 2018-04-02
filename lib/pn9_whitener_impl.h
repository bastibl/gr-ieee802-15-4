/* -*- c++ -*- */
/* 
 * Copyright 2015 Felix Wunsch, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT) <wunsch.felix@googlemail.com>.
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

#ifndef INCLUDED_IEEE802_15_4_PN9_WHITENER_IMPL_H
#define INCLUDED_IEEE802_15_4_PN9_WHITENER_IMPL_H

#include <ieee802_15_4/pn9_whitener.h>

namespace gr {
  namespace ieee802_15_4 {

    class pn9_whitener_impl : public pn9_whitener
    {
     private:
      const static int MAX_PREAMBLE_LEN = 8;
      const static int MAX_SFD_LEN = 4;
      const static int MAX_PHR_LEN = 8;
      const static int MAX_PSDU_LEN = 2048; // Includes CRC, FCS, or MFR
      const static int MAX_PPDU_LEN = MAX_PREAMBLE_LEN + MAX_SFD_LEN + MAX_PHR_LEN + MAX_PSDU_LEN;
      const static int MAX_FCS_LEN = 4; // Same as MFR

      const static int PN9_LEN = (1<<9)/8; // Size of psuedo random sequence in bytes

      unsigned char* d_pn9;

      void pn9_whiten(pmt::pmt_t msg);

     public:
      pn9_whitener_impl(uint16_t seed);
      ~pn9_whitener_impl();
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_PN9_WHITENER_IMPL_H */

