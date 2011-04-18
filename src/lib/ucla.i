/* -*- c++ -*- */

%feature("autodoc", "1");		// generate python docstrings

%include "exception.i"
%import "gnuradio.i"			// the common stuff

%{
#include "gnuradio_swig_bug_workaround.h"	// mandatory bug fix
#include "ucla_cc1k_correlator_cb.h"
#include "ucla_sos_packet_sink.h"
#include "ucla_ieee802_15_4_packet_sink.h"
#include "ucla_qpsk_modulator_cc.h"
#include "ucla_delay_cc.h"
  //#include "ucla_interleave.h"
#include "ucla_multichanneladd_cc.h"
#include "ucla_symbols_to_chips_bi.h"
#include "ucla_manchester_ff.h"
#include <stdexcept>
%}

// ----------------------------------------------------------------

/*
 * First arg is the package prefix.
 * Second arg is the name of the class minus the prefix.
 *
 * This does some behind-the-scenes magic so we can
 * access ucla_cc1k_correlator_cb from python as ucla.cc1k_correlator_cb
 */
GR_SWIG_BLOCK_MAGIC(ucla,cc1k_correlator_cb);

ucla_cc1k_correlator_cb_sptr ucla_make_cc1k_correlator_cb (int payload_bytesize,
						  unsigned char sync_byte, 
						  unsigned char nsync_byte,
						  unsigned char manchester);

class ucla_cc1k_correlator_cb : public gr_block
{
private:
  ucla_cc1k_correlator_cb ();
};

// ----------------------------------------------------------------

GR_SWIG_BLOCK_MAGIC(ucla,sos_packet_sink);

ucla_sos_packet_sink_sptr ucla_make_sos_packet_sink (const std::vector<unsigned char>& sync_vector,
						     gr_msg_queue_sptr target_queue, 
						     int threshold);

class ucla_sos_packet_sink : public gr_sync_block
{
private:
  ucla_cc1k_packet_sink ();
};


GR_SWIG_BLOCK_MAGIC(ucla,ieee802_15_4_packet_sink);

ucla_ieee802_15_4_packet_sink_sptr ucla_make_ieee802_15_4_packet_sink (gr_msg_queue_sptr target_queue, 
							   int threshold);

class ucla_ieee802_15_4_packet_sink : public gr_sync_block
{
private:
  ucla_ieee802_15_4_packet_sink ();
};


GR_SWIG_BLOCK_MAGIC(ucla,qpsk_modulator_cc);

ucla_qpsk_modulator_cc_sptr ucla_make_qpsk_modulator_cc ();

class ucla_qpsk_modulator_cc : public gr_sync_interpolator
{
private:
  ucla_qpsk_modulator_cc ();
};

GR_SWIG_BLOCK_MAGIC(ucla,symbols_to_chips_bi);

ucla_symbols_to_chips_bi_sptr ucla_make_symbols_to_chips_bi ();

class ucla_symbols_to_chips_bi : public gr_sync_interpolator
{
private:
  ucla_symbols_to_chips_bi ();
};


GR_SWIG_BLOCK_MAGIC(ucla,manchester_ff);

ucla_manchester_ff_sptr ucla_make_manchester_ff ();

class ucla_manchester_ff : public gr_sync_interpolator
{
private:
  ucla_manchester_ff ();
};

GR_SWIG_BLOCK_MAGIC(ucla,delay_cc);

ucla_delay_cc_sptr ucla_make_delay_cc (const int delay);

class ucla_delay_cc : public gr_sync_block
{
private:
  ucla_delay_cc ();
};

/*
GR_SWIG_BLOCK_MAGIC(ucla,interleave);

ucla_interleave_sptr ucla_make_interleave (const int delay);

class ucla_interleave : public gr_block
{
private:
  ucla_interleave ();
};
*/

GR_SWIG_BLOCK_MAGIC(ucla,multichanneladd_cc);

ucla_multichanneladd_cc_sptr ucla_make_multichanneladd_cc (const int delay);

class ucla_multichanneladd_cc : public gr_block
{
private:
  ucla_multichanneladd_cc ();
};
