#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import ieee802_15_4 as ieee802_15_4_installed
import ieee802_15_4_swig as ieee802_15_4
import numpy as np
import matplotlib.pyplot as plt

class qa_css_sync (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        print "NOTE: THIS TEST USES THE INSTALLED VERSION OF THE LIBRARY"
        m = ieee802_15_4_installed.css_modulator()
        bits_in, bb_in = m.modulate_random()
        sym_in = m.frame_DQPSK
        print "Number of DQPSK symbols per frame:", len(sym_in)

        zeros = np.zeros((50,))
        data_in = np.concatenate((bb_in, zeros, bb_in, zeros, bb_in, bb_in, bb_in))
        src = blocks.vector_source_c(data_in)
        det = ieee802_15_4.chirp_detector_cc(m.chirp_seq, len(m.time_gap_1), len(m.time_gap_2), 38, 0.95)
        snk_det = blocks.vector_sink_c()
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), -1)
        snk_costas = blocks.vector_sink_c()
        preamble = ieee802_15_4.preamble_detection_cc(len(m.preamble), m.preamble[0])
        snk_preamble = blocks.vector_sink_c()
        self.tb.connect(src, det, costas, preamble)
        self.tb.connect(det, snk_det)
        self.tb.connect(costas, snk_costas)
        self.tb.connect(preamble, snk_preamble)
        self.tb.run()

        ref = np.concatenate((sym_in, sym_in, sym_in))

        det_out = snk_det.data()[:len(sym_in)*3]
        # plt.plot(abs(det_out - ref))
        # plt.title("post chirp detector")
        # plt.show()
        self.assertComplexTuplesAlmostEqual(det_out, ref, 5)

        costas_out = snk_costas.data()[:len(sym_in)*3]
        # plt.plot(abs(costas_out - ref))
        # plt.title("post costas loop")
        # plt.show()
        self.assertComplexTuplesAlmostEqual(costas_out, ref, 5)

        preamble_out = snk_preamble.data()[:len(sym_in)*3]
        f, axarr = plt.subplots(3,1)
        axarr[0].plot(abs(preamble_out - ref))
        axarr[0].set_title("diff preamble costas (abs)")
        axarr[1].plot(np.real(costas_out))
        axarr[1].set_title("real part of costas output")
        axarr[2].plot(np.real(preamble_out))
        axarr[2].set_title("real part of preamble output")
        plt.suptitle("post preamble detector")
        plt.show()
        self.assertComplexTuplesAlmostEqual(preamble_out, ref, 5)


if __name__ == '__main__':
    gr_unittest.run(qa_css_sync)
