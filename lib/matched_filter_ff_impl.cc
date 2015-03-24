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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "matched_filter_ff_impl.h"
#include <volk/volk.h>

namespace gr {
  namespace ieee802_15_4 {

    matched_filter_ff::sptr
    matched_filter_ff::make(std::vector<float> taps)
    {
      return gnuradio::get_initial_sptr
        (new matched_filter_ff_impl(taps));
    }

    /*
     * The private constructor
     */
    matched_filter_ff_impl::matched_filter_ff_impl(std::vector<float> taps)
      : gr::sync_decimator("matched_filter_ff",
              gr::io_signature::make(1,1, sizeof(float)),
              gr::io_signature::make(1,1, sizeof(float)), taps.size()),
      d_taps(taps)
    {
    }

    /*
     * Our virtual destructor.
     */
    matched_filter_ff_impl::~matched_filter_ff_impl()
    {
    }

    int
    matched_filter_ff_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
        const float *in = (const float *) input_items[0];
        float *out = (float *) output_items[0];

        for(int i=0; i<noutput_items; i++)
        {
          volk_32f_x2_dot_prod_32f(out+i, in+i*d_taps.size(), &d_taps[0], d_taps.size());
        }
        
        return noutput_items;
    }

  } /* namespace ieee802_15_4 */
} /* namespace gr */
