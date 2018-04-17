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

#ifndef INCLUDED_IEEE802_15_4_PDU_WRAPPER_IMPL_H
#define INCLUDED_IEEE802_15_4_PDU_WRAPPER_IMPL_H

#include <ieee802_15_4/pdu_wrapper.h>

namespace gr {
  namespace ieee802_15_4 {

    class pdu_wrapper_impl : public pdu_wrapper
    {
     public:
      //const static int MAX_PHR_LEN = 16;


     private:
      const static int MAX_PREAMBLE_LEN = 8;
      const static int MAX_SFD_LEN = 4;
      const static int MAX_PHR_LEN = 16;
      //const static int MAX_PSDU_LEN = 2048; // Includes CRC, FCS, or MFR
      const static int MAX_PPDU_LEN = MAX_PREAMBLE_LEN + MAX_SFD_LEN +
                                    2*MAX_PHR_LEN + GRPW_MAX_PSDU_LEN;
      const static int MAX_FCS_LEN = 4; // Same as MFR

      unsigned char* d_buf;
      unsigned char* d_suffix;
      unsigned char d_prefix_size;
      unsigned char d_suffix_size;

      void wrapper(pmt::pmt_t msg);

     public:
      pdu_wrapper_impl(std::vector<unsigned char> prefix, std::vector<unsigned char> suffix);
      ~pdu_wrapper_impl();
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_PDU_WRAPPER_IMPL_H */

