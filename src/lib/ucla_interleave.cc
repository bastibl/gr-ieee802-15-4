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
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <ucla_interleave.h>
#include <gr_io_signature.h>
#include <string.h>


ucla_interleave_sptr
ucla_make_interleave (size_t itemsize)
{
  return ucla_interleave_sptr (new ucla_interleave (itemsize));
}

ucla_interleave::ucla_interleave (size_t itemsize)
  : gr_block ("interleave",
	      gr_make_io_signature (1, gr_io_signature::IO_INFINITE, itemsize),
	      gr_make_io_signature (1, 1, itemsize)
	      ),
    d_itemsize (itemsize)
{
}

ucla_interleave::~ucla_interleave ()
{
  // NOP
}

void
ucla_interleave::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
  unsigned ninputs = ninput_items_required.size();
  for (unsigned i = 0; i < ninputs; i++)
    ninput_items_required[i] = 0;
}

int
gr_sync_block::general_work (int noutput_items,
			     gr_vector_int &ninput_items,
			     gr_vector_const_void_star &input_items,
			     gr_vector_void_star &output_items)
{
  size_t nchan = input_items.size ();
  int	r = work (noutput_items, input_items, output_items);
  if (r > 0)
    consume_each (r);
  return r;
}

int
ucla_interleave::work (int noutput_items,
		     gr_vector_const_void_star &input_items,
		     gr_vector_void_star &output_items)
{
  size_t nchan = input_items.size ();
  size_t itemsize = d_itemsize;
  const char **in = (const char **) &input_items[0];
  char *out = (char *) output_items[0];

  for (int i = 0; i < noutput_items; i += nchan){
    for (unsigned int n = 0; n < nchan; n++){
      memcpy (out, in[n], itemsize);
      out += itemsize;
      in[n] += itemsize;
    }
  }
  return noutput_items;
}
