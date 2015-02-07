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
#include "preamble_detection_cc_impl.h"

namespace gr {
  namespace ieee802_15_4 {

    preamble_detection_cc::sptr
    preamble_detection_cc::make(int len_preamble, gr_complex preamble_sym)
    {
      return gnuradio::get_initial_sptr
        (new preamble_detection_cc_impl(len_preamble, preamble_sym));
    }

    /*
     * The private constructor
     */
    preamble_detection_cc_impl::preamble_detection_cc_impl(int len_preamble, gr_complex preamble_sym)
      : gr::block("preamble_detection_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_len_preamble(len_preamble),
      d_preamble_sym(preamble_sym),
      d_preamble_detected(false),
      d_phi_off(0.0)
    {
      d_buf = boost::circular_buffer<gr_complex>(d_len_preamble);
      set_output_multiple(len_preamble);
      set_tag_propagation_policy(TPP_DONT);
    }

    /*
     * Our virtual destructor.
     */
    preamble_detection_cc_impl::~preamble_detection_cc_impl()
    {
    }

    void
    preamble_detection_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = noutput_items;
    }

    int
    preamble_detection_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];

        int samples_produced = 0;
        int samples_consumed = 0;

        // check for preamble tag and reset, if found
        std::vector<tag_t> tags;
        get_tags_in_range(tags, 0, nitems_read(0), nitems_read(0) + ninput_items[0], pmt::string_to_symbol("FCP"));
        if(tags.size() > 0)
        {
          uint64_t tag_pos = tags[tags.size()-1].offset - nitems_read(0);
          std::cout << "Preamble detector: found FCP tag at pos " << tags[tags.size()-1].offset << ", consume " << tag_pos << " samples and reset" << std::endl;
          samples_consumed += tag_pos;
          d_preamble_detected = false;
          d_buf.clear();
        }
        else
        {
          dout << "Preamble detector: no tags in range " << nitems_read(0) << " to " << nitems_read(0) + ninput_items[0] << std::endl;
        }

        if(!d_preamble_detected)
        {
          dout << "push samples into buffer: ";
          while(noutput_items - samples_consumed > 0)
          {
            d_buf.push_back(in[samples_consumed]);
            samples_consumed++;
            if(d_buf.size() > 1)
            {
              if(std::abs(std::arg(d_buf[d_buf.size()-1]/d_buf[d_buf.size()-2])) < M_PI/4) // check if new symbol  phase is roughly equal to the last symbol
              {
                dout << ".";
                if(d_buf.full()) // as soon as the buffer is full, a complete preamble has been received
                {
                  std::cout << "Preamble detector: Preamble detected. Start returning symbols." << std::endl;
                  d_preamble_detected = true;
                  if(noutput_items - samples_produced < d_buf.size()) // make sure there is enough space in the output buffer
                    throw std::runtime_error("Output buffer too small");
                  memcpy(out+samples_produced, d_buf.linearize(), sizeof(gr_complex)*d_buf.size()); // copy preamble into the output buffer
                  add_item_tag(0, nitems_written(0) + samples_produced, pmt::string_to_symbol("SOP"), pmt::from_long(0)); // add tag to first samples of preamble
                  d_phi_off = std::arg(d_preamble_sym / d_buf[0]); // calculate phase offset
                  samples_produced += d_buf.size();
                  d_buf.clear();
                  break;
                }
              }
              else // erase all previous symbols if the current is not equal to them
              {
                std::cout << "Preamble detector: Reset after " << d_buf.size() << " equal symbols" << std::endl;
                d_buf.erase(d_buf.begin(), d_buf.begin()+d_buf.size()-1);
              }
            }
          }
          dout << std::endl;
        }

        if(d_preamble_detected)
        {
          dout << "push input buffer directly to output" << std::endl;
          int nsym = std::min(noutput_items - samples_consumed, noutput_items - samples_produced);
          memcpy(out+samples_produced, in+samples_consumed, sizeof(gr_complex)*nsym);
          samples_consumed += nsym;
          samples_produced += nsym;
        }

        // for(int i = 0; i < samples_produced; i++)
        //   out[i] *= std::polar(float(1.0), d_phi_off);
        dout << "consume: " << samples_consumed << ", produce: " << samples_produced << std::endl;
        consume_each (samples_consumed);
        return samples_produced;
    }

  } /* namespace ieee802_15_4 */
} /* namespace gr */

