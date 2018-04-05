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


#ifndef INCLUDED_IEEE802_15_4_SUN_PHR_PREFIXER_H
#define INCLUDED_IEEE802_15_4_SUN_PHR_PREFIXER_H

#include <ieee802_15_4/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace ieee802_15_4 {

    /*!
     * \brief Prepend SUN PHY PHR to PDU
     * \ingroup ieee802_15_4
     *
     * \details
     * Prepends a 2-byte PHR to PDU in an input message, setting
     * Frame Length field to PDU's size.
     *
     * Per section 20.2.2 of 802.15.4-2015.
     * 
     */
    class IEEE802_15_4_API sun_phr_prefixer : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<sun_phr_prefixer> sptr;

      /*!
       * \param fcs True sets FCS Type bit, indicating 2-octet FCS
       * \param dw True sets Data Whitening bit
       */
      static sptr make(bool fcs, bool dw);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_SUN_PHR_PREFIXER_H */

