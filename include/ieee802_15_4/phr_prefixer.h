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


#ifndef INCLUDED_IEEE802_15_4_PHR_PREFIXER_H
#define INCLUDED_IEEE802_15_4_PHR_PREFIXER_H

#include <ieee802_15_4/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace ieee802_15_4 {

    /*!
     * \brief Prepend PHR vector of unsigned char to PDU
     * \ingroup ieee802_15_4
     *
     * \details
     * Unpacks PDU (one bit per char), prepending a configurable
     * vector of unsigned chars. Chars of vector are not unpacked.
     *
     */
    class IEEE802_15_4_API phr_prefixer : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<phr_prefixer> sptr;

      /*!
       * \brief Make a PHR Prefixer block
       *
       */
      static sptr make(std::vector<unsigned char> phr);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_PHR_PREFIXER_H */

