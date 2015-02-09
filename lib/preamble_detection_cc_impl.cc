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
      if(d_len_preamble < 2)
        throw std::runtime_error("Preamble must be at least 2 symbols long");
      d_buf = boost::circular_buffer<gr_complex>(d_len_preamble);
      set_output_multiple(len_preamble*10);
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
          std::cout << "Preamble detector: found FCP tag at pos " << tags[tags.size()-1].offset << std::endl;
          if(d_preamble_detected) // return all samples until the reset happens
          {
            std::cout << "Preamble detector: Return all samples between current position and FCP tag" << std::endl;
            int rem_space_output = noutput_items - samples_produced;
            if(tag_pos <= rem_space_output)
            {
              d_preamble_detected = false;
              d_buf.clear();
              memcpy(out+samples_produced, in+samples_consumed, sizeof(gr_complex)*tag_pos);
              samples_produced += tag_pos;
              samples_consumed += tag_pos;
            }
            else // there are more samples between now and the new tag than we can fit into the output buffer
            {
              memcpy(out+samples_produced, in+samples_consumed, sizeof(gr_complex)*rem_space_output);
              samples_produced += rem_space_output;
              samples_consumed += rem_space_output;              
            }
          }
        }
        else
        {
          std::cout << "Preamble detector: no tags in range " << nitems_read(0) << " to " << nitems_read(0) + ninput_items[0] << std::endl;
        }

        if(!d_preamble_detected)
        {
          while(num_returnable_items(ninput_items[0], noutput_items, samples_consumed, samples_produced) >= 2)
          {
            if(d_buf.size() == 0) // if buffer is empty, push first symbol in
            {
              d_buf.push_back(in[samples_consumed]);
              samples_consumed++;
            }

            // as soon as the buffer is full, a complete preamble has been received. 
            // then wait for the next different symbol that marks the end of the preamble.
            // in case of a late entry there might be leading symbols that are equal to the preamble symbols

            float phase_diff = std::abs(std::arg(in[samples_consumed]/d_buf[d_buf.size()-1]));
            if(phase_diff < M_PI/4 && !d_buf.full()) // buffer is filling and we have a matching symbol phase
            {
              d_buf.push_back(in[samples_consumed]);
              samples_consumed++;
              // std::cout << "Preamble detector: push sample into buffer" << std::endl;
            }
            else if(phase_diff < M_PI/4 && d_buf.full())  // buffer is full and we wait for a different symbol (start of SFD)
            {
              std::cout << "Preamble detector: drop sample waiting for end of preamble" << std::endl;
              samples_consumed++; // drop sample
            }
            else if(phase_diff >= M_PI/4 && !d_buf.full()) // buffer is not full but we already got a different symbol --> no preamble, drop buffer
            {
              // std::cout << "Preamble detector: reset buffer" << std::endl;
              d_buf.clear();
            }
            else // buffer is full and we have a different symbol --> preamble end detected! return buffer and change state to preamble_detected == true
            {
              std::cout << "Preamble detector: Preamble detected. Start returning symbols." << std::endl;
              d_preamble_detected = true;
              if(noutput_items - samples_produced < d_buf.size()) // make sure there is enough space in the output buffer
              {
                std::cout << "noutput_items: " << noutput_items << ", samples_produced: " << samples_produced << ", buffer size: " << d_buf.size() << std::endl;
                throw std::runtime_error("Output buffer too small");
              }
              memcpy(out+samples_produced, d_buf.linearize(), sizeof(gr_complex)*d_buf.size()); // copy preamble into the output buffer
              add_item_tag(0, nitems_written(0) + samples_produced, pmt::string_to_symbol("SOP"), pmt::from_long(0)); // add tag to first samples of preamble
              samples_produced += d_buf.size();
              d_buf.clear();
              break;
            }
          }
        }

        if(d_preamble_detected)
        {
          dout << "push input buffer directly to output" << std::endl;
          int nsym = num_returnable_items(ninput_items[0], noutput_items, samples_consumed, samples_produced);
          memcpy(out+samples_produced, in+samples_consumed, sizeof(gr_complex)*nsym);
          samples_consumed += nsym;
          samples_produced += nsym;
        }

        std::cout << "consume: " << samples_consumed << ", produce: " << samples_produced << std::endl;
        consume_each (samples_consumed);
        return samples_produced;
    }

  } /* namespace ieee802_15_4 */
} /* namespace gr */

