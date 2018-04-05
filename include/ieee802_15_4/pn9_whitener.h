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


#ifndef INCLUDED_IEEE802_15_4_PN9_WHITENER_H
#define INCLUDED_IEEE802_15_4_PN9_WHITENER_H

#include <ieee802_15_4/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace ieee802_15_4 {

    /*!
     * \brief Whiten or unwhiten PDU using PN9 sequence
     * \ingroup ieee802_15_4
     *
     * \details
     * Whitens or unwhitens PDU in input message using PN9 described 
     * in section 17.2.3 of the 802.15.4-2015 specification.
     */
    class IEEE802_15_4_API pn9_whitener : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<pn9_whitener> sptr;

      /*!
       * \param seed Starting seed. Defaults to all ones.
       */
      static sptr make(uint16_t seed = ~0); // SUN PHY default
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_PN9_WHITENER_H */

