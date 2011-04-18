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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <ucla_qpsk_modulator_cc.h>
#include <gr_io_signature.h>
#include <assert.h>

static const int SAMPLES_PER_SYMBOL = 4;

ucla_qpsk_modulator_cc_sptr 
ucla_make_qpsk_modulator_cc ()
{
  return ucla_qpsk_modulator_cc_sptr (new ucla_qpsk_modulator_cc ());
}

ucla_qpsk_modulator_cc::ucla_qpsk_modulator_cc ()
  : gr_sync_interpolator ("qpsk_modulator_cc",
			  gr_make_io_signature (1, 1, sizeof (gr_complex)),
			  gr_make_io_signature (1, 1, sizeof (gr_complex)),
			  SAMPLES_PER_SYMBOL)
{
}

ucla_qpsk_modulator_cc::~ucla_qpsk_modulator_cc()
{
  return;
}

/**
 * Generate a QPSK signal from a +/- 1 float stream. For each
 * two input symbols we output 4 complex symbols with a half-sine
 * pulse shape.
 */
int
ucla_qpsk_modulator_cc::work (int noutput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items)
{
  const gr_complex *in = (gr_complex *) input_items[0];
  gr_complex *out = (gr_complex *) output_items[0];

  assert (noutput_items % SAMPLES_PER_SYMBOL == 0);

  for (int i = 0; i < noutput_items / SAMPLES_PER_SYMBOL; i++){
    float iphase = real(in[i]);
    float qphase = imag(in[i]);
    //fprintf(stderr, "%.0f %.0f ", iphase, qphase), fflush(stderr);

    *out++ = gr_complex(0.0, 0.0);
    *out++ = gr_complex(iphase * 0.70710678, qphase * 0.70710678);
    *out++ = gr_complex(iphase, qphase);
    *out++ = gr_complex(iphase * 0.70710678, qphase * 0.70710678);
  }

  return noutput_items;
}


  
