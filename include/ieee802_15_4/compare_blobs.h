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


#ifndef INCLUDED_IEEE802_15_4_COMPARE_BLOBS_H
#define INCLUDED_IEEE802_15_4_COMPARE_BLOBS_H

#include <ieee802_15_4/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace ieee802_15_4 {

    /*!
     * \brief <+description of block+>
     * \ingroup ieee802_15_4
     *
     */
    class IEEE802_15_4_API compare_blobs : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<compare_blobs> sptr;
      virtual int get_bits_compared() = 0;
      virtual int get_errors_found() = 0;
      virtual float get_ber() = 0;

      /*!
       * \brief Return a shared_ptr to a new instance of ieee802_15_4::compare_blobs.
       *
       * To avoid accidental use of raw pointers, ieee802_15_4::compare_blobs's
       * constructor is in a private implementation
       * class. ieee802_15_4::compare_blobs::make is the public interface for
       * creating new instances.
       */
      static sptr make(bool packet_error_mode=false);
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_COMPARE_BLOBS_H */

