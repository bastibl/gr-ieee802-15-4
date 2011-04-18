/*
Copyright (c) 2006 The Regents of the University of California.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above
   copyright notice, this list of conditions and the following
   disclaimer in the documentation and/or other materials provided
   with the distribution.
3. Neither the name of the University nor that of the Laboratory
   may be used to endorse or promote products derived from this
   software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
*/

#ifndef INCLUDED_UCLA_QPSK_MODULATOR_CC_H
#define INCLUDED_UCLA_QPSK_MODULATOR_CC_H

#include <gr_sync_interpolator.h>
#include <gr_types.h>
#include <gr_io_signature.h>

class ucla_qpsk_modulator_cc;

typedef boost::shared_ptr<ucla_qpsk_modulator_cc> ucla_qpsk_modulator_cc_sptr;

ucla_qpsk_modulator_cc_sptr 
ucla_make_qpsk_modulator_cc ();

/*!
 * \brief Generates a half-sine pulse shape QPSK complex signal
 * from a float input stream. For each 2 input symbols, the block
 * generates four complex output symbols, i.e., it upsamples by a
 * constant factor of 2.
 * \ingroup ucla
 *
 * input: stream of float
 * output: stream of complex
 *
 */

class ucla_qpsk_modulator_cc : public gr_sync_interpolator
{
  friend ucla_qpsk_modulator_cc_sptr ucla_make_qpsk_modulator_cc ();

 protected:
  ucla_qpsk_modulator_cc ();

 public:
  ~ucla_qpsk_modulator_cc();


  int work (int noutput_items,
	    gr_vector_const_void_star &input_items,
	    gr_vector_void_star &output_items);

};

#endif /* INCLUDED_UCLA_QPSK_MODULATOR_CC_H */
