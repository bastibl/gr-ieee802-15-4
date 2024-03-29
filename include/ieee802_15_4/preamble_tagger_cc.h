/* -*- c++ -*- */
/*
 * Copyright 2015 Felix Wunsch, Communications Engineering Lab (CEL) / Karlsruhe Institute
 * of Technology (KIT) <wunsch.felix@googlemail.com>.
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


#ifndef INCLUDED_IEEE802_15_4_PREAMBLE_TAGGER_CC_H
#define INCLUDED_IEEE802_15_4_PREAMBLE_TAGGER_CC_H

#include <gnuradio/sync_block.h>
#include <ieee802_15_4/api.h>

namespace gr {
namespace ieee802_15_4 {

/*!
 * \brief <+description of block+>
 * \ingroup ieee802_15_4
 *
 */
class IEEE802_15_4_API preamble_tagger_cc : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<preamble_tagger_cc> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of ieee802_15_4::preamble_tagger_cc.
     *
     * To avoid accidental use of raw pointers, ieee802_15_4::preamble_tagger_cc's
     * constructor is in a private implementation
     * class. ieee802_15_4::preamble_tagger_cc::make is the public interface for
     * creating new instances.
     */
    static sptr make(int len_preamble);
};

} // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_PREAMBLE_TAGGER_CC_H */
