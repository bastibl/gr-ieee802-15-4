#!/usr/bin/env python

# O-QPSK modulation and demodulation.
#
#
# Copyright 2005 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

# Derived from gmsk.py
#
# Modified by: Thomas Schmid, Leslie Choong, Sanna Leidelof
#

from gnuradio import gr, ucla
from math import pi

class ieee802_15_4_mod(gr.hier_block2):

    def __init__(self, *args, **kwargs):
        """
	Hierarchical block for cc1k FSK modulation.

	The input is a byte stream (unsigned char) and the
	output is the complex modulated signal at baseband.

	@param spb: samples per baud >= 2
	@type spb: integer
	"""
	try:
		self.spb = kwargs.pop('spb')
	except KeyError:
		pass

	gr.hier_block2.__init__(self, "ieee802_15_4_mod",
				gr.io_signature(1, 1, 1),  # Input
				gr.io_signature(1, 1, gr.sizeof_gr_complex))  # Output

        if not isinstance(self.spb, int) or self.spb < 2:
            raise TypeError, "spb must be an integer >= 2"

        self.symbolsToChips = ucla.symbols_to_chips_bi()
        self.chipsToSymbols = gr.packed_to_unpacked_ii(2, gr.GR_MSB_FIRST)
        self.symbolsToConstellation = gr.chunks_to_symbols_ic((-1-1j, -1+1j, 1-1j, 1+1j))

        self.pskmod = ucla.qpsk_modulator_cc()
        self.delay = ucla.delay_cc(self.spb+1)


	# Connect
	self.connect(self, self.symbolsToChips, self.chipsToSymbols,
                   self.symbolsToConstellation, self.pskmod, self.delay, self)

class ieee802_15_4_demod(gr.hier_block2):
    def __init__(self, *args, **kwargs):
        """
        Hierarchical block for O-QPSK demodulation.

        The input is the complex modulated signal at baseband
        and the output is a stream of bytes.

        @param sps: samples per symbol
        @type sps: integer
        """
	try:
		self.sps = kwargs.pop('sps')
	except KeyError:
		pass

	gr.hier_block2.__init__(self, "ieee802_15_4_demod",
				gr.io_signature(1, 1, gr.sizeof_gr_complex),  # Input
				gr.io_signature(1, 1, gr.sizeof_float))  # Output

        # Demodulate FM
        sensitivity = (pi / 2) / self.sps
        #self.fmdemod = gr.quadrature_demod_cf(1.0 / sensitivity)
        self.fmdemod = gr.quadrature_demod_cf(1)

        # Low pass the output of fmdemod to allow us to remove
        # the DC offset resulting from frequency offset

        alpha = 0.0008/self.sps
        self.freq_offset = gr.single_pole_iir_filter_ff(alpha)
        self.sub = gr.sub_ff()
        self.connect(self, self.fmdemod)
        self.connect(self.fmdemod, (self.sub, 0))
        self.connect(self.fmdemod, self.freq_offset, (self.sub, 1))


        # recover the clock
        omega = self.sps
        gain_mu=0.03
        mu=0.5
        omega_relative_limit=0.0002
        freq_error=0.0

        gain_omega = .25*gain_mu*gain_mu        # critically damped
        self.clock_recovery = gr.clock_recovery_mm_ff(omega, gain_omega, mu, gain_mu,
                                                      omega_relative_limit)

        # Connect
        self.connect(self.sub, self.clock_recovery, self)
