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


#ifndef INCLUDED_IEEE802_15_4_PDU_WRAPPER_H
#define INCLUDED_IEEE802_15_4_PDU_WRAPPER_H

#include <ieee802_15_4/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace ieee802_15_4 {

    /*!
     * \brief Prepend vector of unsigned chars to PDU in input message
     * \ingroup ieee802_15_4
     *
     * \details 
     * Prepends or appends a vectors of unsigned char to the PDU on the input message port.
     */

    static const int GRPW_MAX_PSDU_LEN = 2048; // Includes CRC, FCS, or MFR

    class IEEE802_15_4_API pdu_wrapper : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<pdu_wrapper> sptr;

      /*!
       * \param prefix Prefix to prepend, typically a preamble and SFD. Default is for 802.15.4 OQPSK.
       * \param suffix Suffix to append. Default is no pad.
       */
      static sptr make(std::vector<unsigned char> prefix, std::vector<unsigned char> suffix);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_PDU_WRAPPER_H */

