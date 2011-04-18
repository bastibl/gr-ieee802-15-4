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
#ifndef INCLUDED_UCLA_CC1K_CORRELATOR_CB_H
#define INCLUDED_UCLA_CC1K_CORRELATOR_CB_H

#include <gr_block.h>
#include <assert.h>

//#define DEBUG_UCLA_CC1K_CORRELATOR

class ucla_cc1k_correlator_cb;

/*
 * We use boost::shared_ptr's instead of raw pointers for all access
 * to gr_blocks (and many other data structures).  The shared_ptr gets
 * us transparent reference counting, which greatly simplifies storage
 * management issues.  This is especially helpful in our hybrid
 * C++ / Python system.
 *
 * See http://www.boost.org/libs/smart_ptr/smart_ptr.htm
 *
 * As a convention, the _sptr suffix indicates a boost::shared_ptr
 */
typedef boost::shared_ptr<ucla_cc1k_correlator_cb> ucla_cc1k_correlator_cb_sptr;

/*!
 * \brief Return a shared_ptr to a new instance of ucla_cc1k_correlator_cb.
 *
 * To avoid accidental use of raw pointers, ucla_cc1k_correlator_cb's
 * constructor is private.  ucla_make_cc1k_correlator_cb is the public
 * interface for creating new instances.
 */
ucla_cc1k_correlator_cb_sptr ucla_make_cc1k_correlator_cb (int payload_bytesize, unsigned char sync_byte, unsigned char nsync_byte, unsigned char manchester);

/*!
 * \brief implements the cc1k radio chip.
 * \ingroup block
 *
 * \sa ucla_cc1k_correlator_cb for a version that subclasses gr_sync_block.
 */
class ucla_cc1k_correlator_cb : public gr_block
{
private:
  static const int OVERSAMPLE = 8;
  enum state_t { ST_LOOKING, ST_UNDER_THRESHOLD, ST_LOCKED };
  
  int	  	 d_payload_bytesize;
  unsigned char  d_sync_byte;                   // syncronisation byte
  unsigned char  d_nsync_byte;                  // indicates end of sync
  unsigned char  d_manchester;                  // 0: manchester off, 1: manchester on
  state_t	 d_state;
  unsigned int	 d_osi;				// over sample index [0,OVERSAMPLE-1]
  unsigned int	 d_transition_osi;		// first index where Hamming dist < thresh
  unsigned int	 d_center_osi;			// center of bit
  unsigned long long int d_shift_reg[OVERSAMPLE];
  int		 d_bblen;			// length of bitbuf
  float 	*d_bitbuf;			// demodulated bits
  int		 d_bbi;				// bitbuf index

  static const int AVG_PERIOD = 512;		// must be power of 2 (for freq offset correction)
  
  static const unsigned long long CC1K_SYNC = 0x9999999999999999ULL;
  
  static const int CC1K_BITS_PER_BYTE = 8;
  static const int CC1K_SYNC_OVERHEAD = sizeof(CC1K_SYNC);
  static const int CC1K_PAYLOAD_OVERHEAD = 0;		  	// 0 byte overhead
  static const int CC1K_TAIL_PAD = 1;				// one byte trailing padding
  static const int CC1K_OVERHEAD = CC1K_SYNC_OVERHEAD + CC1K_PAYLOAD_OVERHEAD + CC1K_TAIL_PAD; 
  
  static const int THRESHOLD = 3;

  int	d_avbi;
  float	d_avgbuf[AVG_PERIOD];
  float d_avg;
  float d_accum;
  
#ifdef DEBUG_UCLA_CC1K_CORRELATOR
  FILE		*d_debug_fp;			// binary log file
#endif
  
  // The friend declaration allows howto_make_square_ff to
  // access the private constructor.
  
  friend ucla_cc1k_correlator_cb_sptr ucla_make_cc1k_correlator_cb (int payload_bytesize, 
								    unsigned char sync_byte, 
								    unsigned char nsync_byte, 
								    unsigned char manchester);
  
  ucla_cc1k_correlator_cb (int payload_bytesize, 
			   unsigned char sync_byte, 
			   unsigned char nsync_byte, 
			   unsigned char manchester);  	// private constructor
  
  inline int slice (float x)
  {
    return x >= d_avg ? 1 : 0;
  }
  
  void update_avg(float x);
  
  void enter_locked ();
  void enter_under_threshold ();
  void enter_looking ();
  
  static int add_index (int a, int b)
  {
    int t = a + b;
    if (t >= OVERSAMPLE)
      t -= OVERSAMPLE;
    assert (t >= 0 && t < OVERSAMPLE);
    return t;
  }
  
  static int sub_index (int a, int b)
  {
    int t = a - b;
    if (t < 0)
      t += OVERSAMPLE;
    assert (t >= 0 && t < OVERSAMPLE);
    return t;
  }
  
public:
  ~ucla_cc1k_correlator_cb ();	// public destructor
  
  // Where all the action really happens
  
  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};

#endif /* INCLUDED_UCLA_CC1K_CORRELATOR_CB_H */
