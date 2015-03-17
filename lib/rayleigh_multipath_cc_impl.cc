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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "rayleigh_multipath_cc_impl.h"
#include <volk/volk.h>
#include <chrono>

namespace gr {
  namespace ieee802_15_4 {

    rayleigh_multipath_cc::sptr
    rayleigh_multipath_cc::make(std::vector<float> pdp, int coherence_time_samps)
    {
      return gnuradio::get_initial_sptr
        (new rayleigh_multipath_cc_impl(pdp, coherence_time_samps));
    }

    /*
     * The private constructor
     */
    rayleigh_multipath_cc_impl::rayleigh_multipath_cc_impl(std::vector<float> pdp, int coherence_time_samps)
      : gr::sync_block("rayleigh_multipath_cc",
              gr::io_signature::make(1,1, sizeof(gr_complex)),
              gr::io_signature::make(1,1, sizeof(gr_complex))),
      d_pdp(pdp),
      d_coh_time_samps(coherence_time_samps),
      d_samp_ctr(0)
    {
      if(d_coh_time_samps > 0)
        d_is_time_variant = true;
      else
        d_is_time_variant = false;
      d_len_pdp = d_pdp.size();
      normalize_pdp();
      d_taps.assign(d_len_pdp,0);
      d_gen = std::default_random_engine(std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count());
      generate_taps();
      
      set_history(1+d_len_pdp); 
    }

    /*
     * Our virtual destructor.
     */
    rayleigh_multipath_cc_impl::~rayleigh_multipath_cc_impl()
    {
    }

    void
    rayleigh_multipath_cc_impl::normalize_pdp()
    {
      float e = 0;
      for(int i=0; i<d_len_pdp; i++)
        e += d_pdp[i];
      std::cout << "normalized taps: ";
      for(int i=0; i<d_len_pdp; i++)
      {
        d_pdp[i] /= e;
        std::cout << d_pdp[i] << " ";
      }
      std::cout << std::endl;
    }

    void
    rayleigh_multipath_cc_impl::generate_taps()
    {
      // the taps are rayleigh distributed and follow the given PDP
      for(int i=0; i<d_len_pdp; i++)
      {
        double ampl = d_randn(d_gen)*std::sqrt(d_pdp[i]);
        double phi = d_randu(d_gen)*2*M_PI;
        // std::cout << "ampl: " << ampl << ", phi: " << phi << std::endl;
        d_taps[i] = std::polar(ampl, phi);
      }

      // let the first tap have phase 0
      for(int i=0; i<d_len_pdp; i++)
      {
        d_taps[i] *= std::polar(float(1.0),-std::arg(d_taps[0]));
      }

      // reverse the tap order for easier convolution via volk dot product
      std::reverse(d_taps.begin(), d_taps.end());
    }

    int
    rayleigh_multipath_cc_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];

        for(int i=0; i<noutput_items; i++)
        {
          volk_32fc_x2_dot_prod_32fc(out+i, in+i, &d_taps[0], d_len_pdp); 
          d_samp_ctr++;
          if(d_samp_ctr >= d_coh_time_samps && d_is_time_variant)
          {
            generate_taps();  
            d_samp_ctr = 0;     
          }
        }

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace ieee802_15_4 */
} /* namespace gr */
