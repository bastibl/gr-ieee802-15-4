/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <ucla_delay_cc.h>

// public constructor
ucla_delay_cc_sptr 
ucla_make_delay_cc (const int delay) 
{
  return ucla_delay_cc_sptr (new ucla_delay_cc (delay));
}

ucla_delay_cc::ucla_delay_cc (const int delay)
  : gr_sync_block ("delay_cc",
		   gr_make_io_signature (1, 1, sizeof (gr_complex)),
		   gr_make_io_signature (1, 1, sizeof (gr_complex)))
{
  d_delay = delay;
  set_history (delay);
}

ucla_delay_cc::~ucla_delay_cc ()
{
  return;
}

int
ucla_delay_cc::work (int noutput_items,
		     gr_vector_const_void_star &input_items,
		     gr_vector_void_star &output_items)
{
  gr_complex *in = (gr_complex *) input_items[0];
  gr_complex *out = (gr_complex *) output_items[0];

  //fprintf(stderr, "."), fflush(stderr);
  for (int j = 0; j < noutput_items; j++)
      out[j] = gr_complex (real(in[j]), imag(in[j-d_delay]));

  return noutput_items;
}
