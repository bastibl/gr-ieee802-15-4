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
#include "dqcsk_mapper_fc_impl.h"
#include <volk/volk.h>

namespace gr {
  namespace ieee802_15_4 {

    dqcsk_mapper_fc::sptr
    dqcsk_mapper_fc::make(std::vector<gr_complex> chirp_seq, std::vector<gr_complex> time_gap_1, std::vector<gr_complex> time_gap_2, int len_subchirp, int num_subchirps)
    {
      return gnuradio::get_initial_sptr
        (new dqcsk_mapper_fc_impl(chirp_seq, time_gap_1, time_gap_2, len_subchirp, num_subchirps));
    }

    /*
     * The private constructor
     */
    dqcsk_mapper_fc_impl::dqcsk_mapper_fc_impl(std::vector<gr_complex> chirp_seq, std::vector<gr_complex> time_gap_1, std::vector<gr_complex> time_gap_2, int len_subchirp, int num_subchirps)
      : gr::block("dqcsk_mapper_fc",
              gr::io_signature::make(1,1, sizeof(float)),
              gr::io_signature::make(1,1, sizeof(gr_complex))),
      d_chirp_seq(chirp_seq),
      d_time_gap_1(time_gap_1),
      d_time_gap_2(time_gap_2),
      d_len_subchirp(len_subchirp),
      d_num_subchirps(num_subchirps),
      d_chirp_seq_ctr(0)
    {
      set_output_multiple(4*d_len_subchirp+d_time_gap_2.size());
    }

    /*
     * Our virtual destructor.
     */
    dqcsk_mapper_fc_impl::~dqcsk_mapper_fc_impl()
    {}

    void
    dqcsk_mapper_fc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = d_num_subchirps; 
    }

    int
    dqcsk_mapper_fc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const float *in = (const float*) input_items[0];
        gr_complex *out = (gr_complex*) output_items[0];

        // std::cout << "work called with " << ninput_items[0] << " input and " << noutput_items << " output items" << std::endl;
        // std::cout << "input buffer:";
        // for(int i=0; i<ninput_items[0]; i++)
        //   std::cout << " " << in[i];
        // std::cout << std::endl;

        for(int i=0; i<d_num_subchirps; i++)
          volk_32fc_s32fc_multiply_32fc(out+i*d_len_subchirp, &d_chirp_seq[d_len_subchirp*i], std::polar(float(1.0),in[i]), d_len_subchirp);
       
        int nitems_written = d_num_subchirps*d_len_subchirp;
        
        if(d_chirp_seq_ctr % 2 == 0)
        {
          // std::cout << "insert tg1" << std::endl;
          memcpy(out+nitems_written, &d_time_gap_1[0], sizeof(gr_complex)*d_time_gap_1.size());
          nitems_written += d_time_gap_1.size();          
        }
        else
        {
          // std::cout << "insert tg2" << std::endl;
          memcpy(out+nitems_written, &d_time_gap_2[0], sizeof(gr_complex)*d_time_gap_2.size());
          nitems_written += d_time_gap_2.size();              
        }
        d_chirp_seq_ctr = (d_chirp_seq_ctr+1) % 2;


        // std::cout << "return with " << d_num_subchirps << " consumed and " << nitems_written << " output items" << std::endl;

        consume_each(d_num_subchirps);
        return nitems_written;
    }

  } /* namespace ieee802_15_4 */
} /* namespace gr */

