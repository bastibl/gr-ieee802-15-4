/* -*- c++ -*- */
/*
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <ucla_manchester_ff.h>
#include <gr_io_signature.h>
#include <assert.h>
#include <iostream>
#include <cstring>

ucla_manchester_ff_sptr
ucla_make_manchester_ff ()
{
  return ucla_manchester_ff_sptr (new ucla_manchester_ff ());
}

ucla_manchester_ff::ucla_manchester_ff ()
  : gr_sync_interpolator ("manchester_ff",
			  gr_make_io_signature (1, -1, sizeof (float)),
			  gr_make_io_signature (1, -1, sizeof (float)),
			  16) // this is actually an interpolation of 8 since manchaster encoding makes one input two 2 outputs.
{
}

int
ucla_manchester_ff::work (int noutput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items)
{
  assert (input_items.size() == output_items.size());
  int nstreams = input_items.size();

  //fprintf(stderr, "\n-- %d, %d\n", noutput_items, nstreams);

  for (int m=0;m<nstreams;m++) {
    float out1;
    float out2;
    const float *in = (float *) input_items[m];
    float *out = (float *) output_items[m];
    // per stream processing
    for (int i = 0; i < noutput_items; i+=16){
      //fprintf(stderr, "%f ", in[i/16]), fflush(stderr);
      
      if(in[i/16] > 0.0){
	out1 = 1.0;
	out2 = 0.0;
      } else {
	out1 = 0.0;
	out2 = 1.0;
      }
      //create manchester output and upsample by 8
      for (int j = 0; j<8; j++){
	memcpy(&out[i+j], &out1, sizeof(float));
      }
      for (int j = 8; j<16; j++){
	memcpy(&out[i+j], &out2, sizeof(float));
      }

      //for (int j = 0; j<16; j++){
      //fprintf(stderr, "%f", out[i/16+j]);
      //}
    }
    // end of per stream processing

  }
  return noutput_items;
}
