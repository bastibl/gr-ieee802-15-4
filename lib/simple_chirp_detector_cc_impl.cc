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
#include "simple_chirp_detector_cc_impl.h"
#include <volk/volk.h>


namespace gr {
  namespace ieee802_15_4 {

    simple_chirp_detector_cc::sptr
    simple_chirp_detector_cc::make(std::vector<gr_complex> chirp_seq, int time_gap_1, int time_gap_2, int len_subchirp, float threshold)
    {
      return gnuradio::get_initial_sptr
        (new simple_chirp_detector_cc_impl(chirp_seq, time_gap_1, time_gap_2, len_subchirp, threshold));
    }

    /*
     * The private constructor
     */
    simple_chirp_detector_cc_impl::simple_chirp_detector_cc_impl(std::vector<gr_complex> chirp_seq, int time_gap_1, int time_gap_2, int len_subchirp, float threshold)
      : gr::block("simple_chirp_detector_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_chirp_seq(chirp_seq),
      d_time_gap_1(time_gap_1),
      d_time_gap_2(time_gap_2),
      d_len_subchirp(len_subchirp),
      d_threshold(threshold)
    {
      if(d_chirp_seq.size() != 4*d_len_subchirp)
        throw std::runtime_error("Chirp sequence has invalid length");

      // calculate energy per subchirp
      volk_32fc_x2_conjugate_dot_prod_32fc(&d_e_subchirp, &d_chirp_seq[0], &d_chirp_seq[0], d_len_subchirp);
    }

    /*
     * Our virtual destructor.
     */
    simple_chirp_detector_cc_impl::~simple_chirp_detector_cc_impl()
    {
    }

    void
    simple_chirp_detector_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = d_len_subchirp;
    }

    gr_complex
    simple_chirp_detector_cc_impl::correlate_with_subchirp(const gr_complex* buf, int chirp_number)
    {
      gr_complex corrval = 0;
      volk_32fc_x2_conjugate_dot_prod_32fc(&corrval, buf, &d_chirp_seq[chirp_number*d_len_subchirp], d_len_subchirp);
      gr_complex e_buf = 0;
      volk_32fc_x2_conjugate_dot_prod_32fc(&e_buf, buf, buf, d_len_subchirp);
      // dout << "correlation result:" << corrval << "/" << std::sqrt(e_buf*d_e_subchirp) << "=> norm = " << std::norm(corrval/(std::sqrt(e_buf*d_e_subchirp)+gr_complex(1e-6,0))) << std::endl;
      // normalize using standard deviations of both signals (assuming mean==0)
      // add 1e-6 to avoid divide-by-zero errors
      return corrval/(std::sqrt(e_buf*d_e_subchirp)+gr_complex(1e-6,0)); 
    }

    bool 
    simple_chirp_detector_cc_impl::corr_over_threshold(gr_complex corrval)
    {
      if(std::norm(corrval) > d_threshold)
        return true;
      else
        return false;
    }

    int
    simple_chirp_detector_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];

        int samples_consumed = 0;
        int samples_produced = 0;

        bool sym_found = false;
        for(int n=0; n<4; n++)
        {
          gr_complex sym = correlate_with_subchirp(in, n);
          if(corr_over_threshold(sym))
          {
            samples_consumed += d_len_subchirp;
            out[samples_produced] = sym;
            samples_produced++;
            sym_found = true;
            break;
          }          
        }

        if(!sym_found)
        {
          samples_consumed++;
        }
        
        // std::cout << "consume: " << samples_consumed << "/" << ninput_items[0] << std::endl;
        // std::cout << "produce: " << samples_produced << "/" << noutput_items << std::endl;
        consume_each (samples_consumed);
        return samples_produced;
    }

  } /* namespace ieee802_15_4 */
} /* namespace gr */

