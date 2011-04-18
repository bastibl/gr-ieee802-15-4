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

#ifndef INCLUDED_UCLA_MANCHESTER_FF_H
#define INCLUDED_UCLA_MANCHESTER_FF_H

#include <gr_sync_interpolator.h>

class ucla_manchester_ff;
typedef boost::shared_ptr<ucla_manchester_ff> ucla_manchester_ff_sptr;

ucla_manchester_ff_sptr ucla_make_manchester_ff ();

/*!
 * \brief
 * \ingroup ucla
 *
 * input:
 *
 */

class ucla_manchester_ff : public gr_sync_interpolator
{
  friend ucla_manchester_ff_sptr ucla_make_manchester_ff ();

  ucla_manchester_ff();

 public:
  int work (int noutput_items,
	    gr_vector_const_void_star &input_items,
	    gr_vector_void_star &output_items);

  bool check_topology(int ninputs, int noutputs) { return ninputs == noutputs; }
};

#endif
