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
#include "costas_loop_cc_impl.h"

namespace gr {
  namespace ieee802_15_4 {

    costas_loop_cc::sptr
    costas_loop_cc::make(std::vector<gr_complex> constellation_points, int initial_index)
    {
      return gnuradio::get_initial_sptr
        (new costas_loop_cc_impl(constellation_points, initial_index));
    }

    /*
     * The private constructor
     */
    costas_loop_cc_impl::costas_loop_cc_impl(std::vector<gr_complex> constellation_points, int initial_index)
      : gr::sync_block("costas_loop_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_const(constellation_points),
      d_initial_index(initial_index),
      d_M(constellation_points.size()),
      d_last_index(FIRST_RUN)
    {
      d_diff = new float[d_M];
    }

    /*
     * Our virtual destructor.
     */
    costas_loop_cc_impl::~costas_loop_cc_impl()
    {
      delete[] d_diff;
    }

    void 
    costas_loop_cc_impl::reset()
    {
      d_phase_offset = 0;
      d_last_index = FIRST_RUN;
    }

    int
    costas_loop_cc_impl::get_nearest_index(gr_complex p)
    {
      dout << "\t diff angles between " << p << " and constellation points: " << std::endl;;
      for(int k = 0; k < d_M; k++)
      {
        d_diff[k] = std::arg(p/d_const[k]);
        dout << "\t\t" << "arg(" << p << "/" << d_const[k] << "=" << d_diff[k] << std::endl;
      }
      dout << std::endl;
      int min_ind = 0;
      for(int k = 1; k < d_M; k++)
      {
        if(std::abs(d_diff[k]) < std::abs(d_diff[min_ind]))
        {
          dout << "\t" << std::abs(d_diff[k]) << "<" << std::abs(d_diff[min_ind]) << std::endl;
          min_ind = k;
        }
      }
      return min_ind;
    }

    int
    costas_loop_cc_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];

        for(int i = 0; i < noutput_items; i++)
        {
          if(d_last_index == FIRST_RUN)
          {
            if(d_initial_index != NO_INIT_PHASE) // assign first incoming symbol to a fixed constellation point
            {
              dout << "First run, initialize phase offset as angular distance to index " << d_initial_index << std::endl;
              d_phase_offset = std::arg(in[i]/d_const[d_initial_index]);
              out[i] = d_const[d_initial_index];
              d_last_index = d_initial_index;
            }
            else // choose nearest constellation point
            {
              dout << "First run, initialize phase offset as angular distance to nearest constellation symbol" << std::endl;
              int nearest_sym_index = get_nearest_index(in[i]);
              dout << "Nearest symbol index: " << nearest_sym_index << std::endl;
              d_phase_offset = d_diff[nearest_sym_index];
              out[i] = d_const[nearest_sym_index];
              d_last_index = nearest_sym_index;
            }
          }
          else // shift with last phase offset and assign incoming symbol to the next nearest constellation point
          {
            dout << "shift phase offset to nearest constellation symbol" << std::endl;
            gr_complex sym = in[i] * std::polar(float(1.0), -d_phase_offset);
            int nearest_sym_index = get_nearest_index(sym);
            dout << "Nearest symbol index: " << nearest_sym_index << std::endl;
            out[i] = sym * std::polar(float(1.0), d_diff[nearest_sym_index]);
            d_phase_offset = fmod(d_phase_offset + d_diff[nearest_sym_index], 2*M_PI);
            d_last_index = nearest_sym_index;
          }
          dout << "input symbol: " << in[i] << ",return symbol: " << out[i] << ", phase offset: " << d_phase_offset << " rad" << std::endl;
        }

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace ieee802_15_4 */
} /* namespace gr */

