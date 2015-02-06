/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
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
#include "frame_buffer_cc_impl.h"

namespace gr {
  namespace ieee802_15_4 {

    frame_buffer_cc::sptr
    frame_buffer_cc::make(int nsym_frame)
    {
      return gnuradio::get_initial_sptr
        (new frame_buffer_cc_impl(nsym_frame));
    }

    /*
     * The private constructor
     */
    frame_buffer_cc_impl::frame_buffer_cc_impl(int nsym_frame)
      : gr::block("frame_buffer_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_nsym_frame(nsym_frame)
    {
      d_buf.clear();
      set_output_multiple(d_nsym_frame);
    }

    /*
     * Our virtual destructor.
     */
    frame_buffer_cc_impl::~frame_buffer_cc_impl()
    {
    }

    void
    frame_buffer_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    }

    int
    frame_buffer_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];

        int samples_consumed = 0;
        int samples_produced = 0;
        int samples_available = ninput_items[0];

        std::vector<tag_t> tags;
        get_tags_in_range(tags, 0, nitems_read(0), nitems_read(0) + ninput_items[0], pmt::string_to_symbol("SOP"));
        if(tags.size() > 0)
        {
          //FIXME
        }

        while(samples_available > 0)
        {
          d_buf.push_back(in[samples_consumed]);
          samples_consumed++;
          samples_available--;
          if(d_buf.size() == d_nsym_frame)
          {
            std::cout << "Complete frame received, return samples" << std::endl;
            memcpy(out, in, sizeof(gr_complex)*d_nsym_frame);
            d_buf.clear();
            samples_produced += d_nsym_frame;
          }
        }

        consume_each (samples_consumed);
        return samples_produced;
    }

  } /* namespace ieee802_15_4 */
} /* namespace gr */

