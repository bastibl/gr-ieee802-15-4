#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 Felix Wunsch, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT) <wunsch.felix@googlemail.com>.
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

    def test_001_t (self): # full frames with zeros inbetween
        print "NOTE: THIS TEST USES THE INSTALLED VERSION OF THE LIBRARY"
        print "Test complete frames with zeros inbetween"
        m = ieee802_15_4_installed.css_modulator()
        bits_in, bb_in = m.modulate_random()
        sym_in = m.frame_DQPSK
        print "Number of DQPSK symbols per frame:", len(sym_in)

        zeros = np.zeros((50,))
        data_in = np.concatenate((bb_in, zeros, bb_in, zeros, bb_in, bb_in, bb_in, bb_in))
        src = blocks.vector_source_c(data_in)
        det = ieee802_15_4.simple_chirp_detector_cc(m.chirp_seq, len(m.time_gap_1), len(m.time_gap_2), 38, 0.95)
        snk_det = blocks.vector_sink_c()
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), -1)
        snk_costas = blocks.vector_sink_c()
        preamble = ieee802_15_4.preamble_tagger_cc(len(m.preamble))
        snk_preamble = blocks.vector_sink_c()
        frame_buffer = ieee802_15_4.frame_buffer_cc(len(sym_in))
        snk_framebuffer = blocks.vector_sink_c()
        self.tb.connect(src, det, costas, preamble, frame_buffer)
        self.tb.connect(det, snk_det)
        self.tb.connect(costas, snk_costas)
        self.tb.connect(preamble, snk_preamble)
        self.tb.connect(frame_buffer, snk_framebuffer)
        self.tb.run()

        ref = np.concatenate((sym_in, sym_in, sym_in))

        # det_out = snk_det.data()[:len(sym_in)*3]
        # # plt.plot(abs(det_out - ref))
        # # plt.title("post chirp detector")
        # # plt.show()
        # self.assertComplexTuplesAlmostEqual(det_out, ref, 5)

        # costas_out = snk_costas.data()[:len(sym_in)*3]
        # # plt.plot(abs(costas_out - ref))
        # # plt.title("post costas loop")
        # # plt.show()
        # self.assertComplexTuplesAlmostEqual(costas_out, ref, 5)

        # preamble_out = snk_preamble.data()[:len(sym_in)*3]
        framebuffer_out = snk_framebuffer.data()[:len(sym_in)*3]

        # print "len(data_in):", len(data_in)
        # print "len(det_out):", len(det_out)
        # print "len(costas_out):", len(costas_out)
        # print "len(preamble_out):", len(preamble_out)
        # print "len(framebuffer_out):", len(framebuffer_out)

        # f, axarr = plt.subplots(3,1)
        # axarr[0].plot(abs(framebuffer_out - ref))
        # axarr[0].set_title("diff preamble ref (abs)")
        # axarr[1].plot(np.real(det_out))
        # axarr[1].set_title("real part of chirp det output")
        # axarr[2].plot(np.real(framebuffer_out))
        # axarr[2].set_title("real part of frambuffer output")
        # plt.suptitle("post framebuffer")
        # plt.show()
        self.assertComplexTuplesAlmostEqual(framebuffer_out, ref, 5)

    def test_002_t (self): # zeros before signal
        print "NOTE: THIS TEST USES THE INSTALLED VERSION OF THE LIBRARY"
        print "Test delayed signal start"
        m = ieee802_15_4_installed.css_modulator()
        bits_in1, bb_in1 = m.modulate_random()
        sym_in1 = m.frame_DQPSK
        bits_in2, bb_in2 = m.modulate_random()
        sym_in2 = m.frame_DQPSK
        bits_in3, bb_in3 = m.modulate_random()
        sym_in3 = m.frame_DQPSK
        print "Number of DQPSK symbols per frame:", len(sym_in1)

        zeros = np.zeros((50,))
        data_in = np.concatenate((zeros, bb_in1, bb_in2, bb_in3, bb_in3, bb_in3, bb_in3, bb_in3))
        src = blocks.vector_source_c(data_in)
        det = ieee802_15_4.simple_chirp_detector_cc(m.chirp_seq, len(m.time_gap_1), len(m.time_gap_2), 38, 0.95)
        snk_det = blocks.vector_sink_c()
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), -1)
        snk_costas = blocks.vector_sink_c()
        preamble = ieee802_15_4.preamble_tagger_cc(len(m.preamble))
        snk_preamble = blocks.vector_sink_c()
        frame_buffer = ieee802_15_4.frame_buffer_cc(len(sym_in1))
        snk_framebuffer = blocks.vector_sink_c()
        self.tb.connect(src, det, costas, preamble, frame_buffer)
        self.tb.connect(det, snk_det)
        self.tb.connect(costas, snk_costas)
        self.tb.connect(preamble, snk_preamble)
        self.tb.connect(frame_buffer, snk_framebuffer)
        self.tb.run()

        ref = np.concatenate((sym_in1, sym_in2, sym_in3))

        # det_out = snk_det.data()[:len(sym_in1)*3]
        # self.assertComplexTuplesAlmostEqual(det_out, ref, 5)

        # costas_out = snk_costas.data()[:len(sym_in1)*3]
        # self.assertComplexTuplesAlmostEqual(costas_out, ref, 5)

        # preamble_out = snk_preamble.data()[:len(sym_in1)*3]
        # self.assertComplexTuplesAlmostEqual(preamble_out, ref, 5)

        framebuffer_out = snk_framebuffer.data()[:len(sym_in1)*3]
        self.assertComplexTuplesAlmostEqual(framebuffer_out, ref, 5)

    def test_003_t (self): # late entry
        print "NOTE: THIS TEST USES THE INSTALLED VERSION OF THE LIBRARY"
        print "Test late entry"
        m = ieee802_15_4_installed.css_modulator()
        bits_in1, bb_in1 = m.modulate_random()
        sym_in1 = m.frame_DQPSK
        bits_in2, bb_in2 = m.modulate_random()
        sym_in2 = m.frame_DQPSK
        bits_in3, bb_in3 = m.modulate_random()
        sym_in3 = m.frame_DQPSK
        print "Number of DQPSK symbols per frame:", len(sym_in1)

        zeros = np.zeros((50,))
        nsym_early = 9
        # data_part = np.concatenate((bb_in1[-nsym_early*192/4:], bb_in1, bb_in2, bb_in3, bb_in3, bb_in3))
        data_part = np.concatenate((bb_in1[-2*192-70-38-10:], bb_in1, bb_in2, bb_in3, bb_in3, bb_in3))
        ncopies = 1
        data = np.tile(data_part, (ncopies,))
        data_in = np.concatenate((data, bb_in3, bb_in3, bb_in3))
        src = blocks.vector_source_c(data_in)
        det = ieee802_15_4.simple_chirp_detector_cc(m.chirp_seq, len(m.time_gap_1), len(m.time_gap_2), 38, 0.95)
        snk_det = blocks.vector_sink_c()
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), -1)
        snk_costas = blocks.vector_sink_c()
        preamble = ieee802_15_4.preamble_tagger_cc(len(m.preamble))
        snk_preamble = blocks.vector_sink_c()
        frame_buffer = ieee802_15_4.frame_buffer_cc(len(sym_in1))
        snk_framebuffer = blocks.vector_sink_c()
        self.tb.connect(src, det, costas, preamble, frame_buffer)
        self.tb.connect(det, snk_det)
        self.tb.connect(costas, snk_costas)
        self.tb.connect(preamble, snk_preamble)
        self.tb.connect(frame_buffer, snk_framebuffer)
        self.tb.run()

        ref_len = (len(sym_in1)*3 + nsym_early)*ncopies
        det_out = snk_det.data()[:ref_len]
        ref_det_part = np.concatenate((sym_in1[-nsym_early:], sym_in1, sym_in2, sym_in3))
        ref_det = np.tile(ref_det_part, (ncopies,))
        self.assertComplexTuplesAlmostEqual(det_out, ref_det, 5)

        costas_out = snk_costas.data()[:ref_len]
        ref_costas = ref_det
        self.assertComplexTuplesAlmostEqual(costas_out, ref_costas, 5)

        preamble_out = snk_preamble.data()[:ref_len]
        ref_preamble = ref_costas
        self.assertComplexTuplesAlmostEqual(preamble_out, ref_preamble, 5)
        
        framebuffer_out = snk_framebuffer.data()[:ref_len-ncopies*nsym_early]
        ref_framebuffer_part = np.concatenate((sym_in1, sym_in2, sym_in3))
        ref_framebuffer = np.tile(ref_framebuffer_part, (ncopies,))

        self.assertComplexTuplesAlmostEqual(framebuffer_out, ref_framebuffer, 5)

    def test_004_t (self):
        print "NOTE: THIS TEST USES THE INSTALLED VERSION OF THE LIBRARY"
        print "Test interrupted frames at symbol boundary without zeros inbetween"
        m = ieee802_15_4_installed.css_modulator()
        bits_in1, bb_in1 = m.modulate_random()
        len_bb = len(bb_in1)
        sym_in1 = m.frame_DQPSK
        len_frame = len(sym_in1)
        bits_in2, bb_in2 = m.modulate_random()
        sym_in2 = m.frame_DQPSK
        bits_in3, bb_in3 = m.modulate_random()
        sym_in3 = m.frame_DQPSK
        print "Number of DQPSK symbols per frame:", len(sym_in1)

        zeros = np.zeros((50000,))
        data_part = np.concatenate((bb_in1, bb_in2[:len_bb/2], bb_in2, bb_in3))
        ncopies = 10
        data = np.tile(data_part, (ncopies,))
        data_in = np.concatenate((data, bb_in3, bb_in3, bb_in3)) # pad some frames
        src = blocks.vector_source_c(data_in)
        det = ieee802_15_4.simple_chirp_detector_cc(m.chirp_seq, len(m.time_gap_1), len(m.time_gap_2), 38, 0.999)
        snk_det = blocks.vector_sink_c()
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), -1)
        snk_costas = blocks.vector_sink_c()
        preamble = ieee802_15_4.preamble_tagger_cc(len(m.preamble))
        snk_preamble = blocks.vector_sink_c()
        frame_buffer = ieee802_15_4.frame_buffer_cc(len(sym_in1))
        snk_framebuffer = blocks.vector_sink_c()
        self.tb.connect(src, det, costas, preamble, frame_buffer)
        self.tb.connect(det, snk_det)
        self.tb.connect(costas, snk_costas)
        self.tb.connect(preamble, snk_preamble)
        self.tb.connect(frame_buffer, snk_framebuffer)
        self.tb.run()

        ref_len = int(len_frame*3.5*ncopies)
        det_out = snk_det.data()[:ref_len]
        ref_det_part = np.concatenate((sym_in1, sym_in2[:len_frame/2], sym_in2, sym_in3))
        ref_det = np.tile(ref_det_part, (ncopies,))
        self.assertComplexTuplesAlmostEqual(det_out, ref_det, 5)

        costas_out = snk_costas.data()[:ref_len]
        ref_costas = ref_det
        self.assertComplexTuplesAlmostEqual(costas_out, ref_costas, 5)

        preamble_out = snk_preamble.data()[:ref_len]
        ref_preamble = ref_costas
        self.assertComplexTuplesAlmostEqual(preamble_out, ref_preamble, 5)

        framebuffer_out = snk_framebuffer.data()[:ref_len-ncopies*len_frame/2]
        ref_framebuffer_part = np.concatenate((sym_in1, sym_in2, sym_in3))
        ref_framebuffer = np.tile(ref_framebuffer_part, (ncopies,))

        self.assertComplexTuplesAlmostEqual(framebuffer_out, ref_framebuffer, 5)       

    def test_005_t (self):
        print "NOTE: THIS TEST USES THE INSTALLED VERSION OF THE LIBRARY"
        print "Test interrupted frames at symbol boundary with zeros inbetween"
        m = ieee802_15_4_installed.css_modulator()
        bits_in1, bb_in1 = m.modulate_random()
        len_bb = len(bb_in1)
        sym_in1 = m.frame_DQPSK
        len_frame = len(sym_in1)
        bits_in2, bb_in2 = m.modulate_random()
        sym_in2 = m.frame_DQPSK
        bits_in3, bb_in3 = m.modulate_random()
        sym_in3 = m.frame_DQPSK
        print "Number of DQPSK symbols per frame:", len(sym_in1)

        zeros = np.zeros((100,))
        data_part = np.concatenate((bb_in1, bb_in2[:192*30], zeros, bb_in2[192*30:], bb_in3))
        ncopies = 10
        data = np.tile(data_part, (ncopies,))
        data_in = np.concatenate((data, bb_in3, bb_in3, bb_in3)) # pad some frames
        src = blocks.vector_source_c(data_in)
        det = ieee802_15_4.simple_chirp_detector_cc(m.chirp_seq, len(m.time_gap_1), len(m.time_gap_2), 38, 0.999)
        snk_det = blocks.vector_sink_c()
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), -1)
        snk_costas = blocks.vector_sink_c()
        preamble = ieee802_15_4.preamble_tagger_cc(len(m.preamble))
        snk_preamble = blocks.vector_sink_c()
        frame_buffer = ieee802_15_4.frame_buffer_cc(len(sym_in1))
        snk_framebuffer = blocks.vector_sink_c()
        self.tb.connect(src, det, costas, preamble, frame_buffer)
        self.tb.connect(det, snk_det)
        self.tb.connect(costas, snk_costas)
        self.tb.connect(preamble, snk_preamble)
        self.tb.connect(frame_buffer, snk_framebuffer)
        self.tb.run()

        ref_len = len_frame*3*ncopies
        det_out = snk_det.data()[:ref_len]
        ref_det_part = np.concatenate((sym_in1, sym_in2, sym_in3))
        ref_det = np.tile(ref_det_part, (ncopies,))
        self.assertComplexTuplesAlmostEqual(det_out, ref_det, 5)

        costas_out = snk_costas.data()[:ref_len]
        ref_costas = ref_det
        self.assertComplexTuplesAlmostEqual(costas_out, ref_costas, 5)

        preamble_out = snk_preamble.data()[:ref_len]
        ref_preamble = ref_costas
        self.assertComplexTuplesAlmostEqual(preamble_out, ref_preamble, 5)

        framebuffer_out = snk_framebuffer.data()[:ref_len]
        ref_framebuffer_part = np.concatenate((sym_in1, sym_in2, sym_in3))
        ref_framebuffer = np.tile(ref_framebuffer_part, (ncopies,))

        self.assertComplexTuplesAlmostEqual(framebuffer_out, ref_framebuffer, 5) 

    def test_006_t (self):
        print "NOTE: THIS TEST USES THE INSTALLED VERSION OF THE LIBRARY"
        print "Test interrupted frames during chirp ramp with zeros inbetween (fading)"
        m = ieee802_15_4_installed.css_modulator()
        bits_in1, bb_in1 = m.modulate_random()
        len_bb = len(bb_in1)
        sym_in1 = m.frame_DQPSK
        len_frame = len(sym_in1)
        bits_in2, bb_in2 = m.modulate_random()
        sym_in2 = m.frame_DQPSK
        bits_in3, bb_in3 = m.modulate_random()
        sym_in3 = m.frame_DQPSK
        print "Number of DQPSK symbols per frame:", len(sym_in1)

        zeros = np.ones((5000,))
        data_in = np.concatenate((bb_in1[:192*30-25], zeros, bb_in1[192*30+24:], bb_in2, bb_in1, bb_in2, bb_in3, bb_in3, bb_in3))
        src = blocks.vector_source_c(data_in)
        det = ieee802_15_4.simple_chirp_detector_cc(m.chirp_seq, len(m.time_gap_1), len(m.time_gap_2), 38, 0.999)
        snk_det = blocks.vector_sink_c()
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), -1)
        snk_costas = blocks.vector_sink_c()
        preamble = ieee802_15_4.preamble_tagger_cc(len(m.preamble))
        snk_preamble = blocks.vector_sink_c()
        frame_buffer = ieee802_15_4.frame_buffer_cc(len(sym_in1))
        snk_framebuffer = blocks.vector_sink_c()
        self.tb.connect(src, det, costas, preamble, frame_buffer)
        self.tb.connect(det, snk_det)
        self.tb.connect(costas, snk_costas)
        self.tb.connect(preamble, snk_preamble)
        self.tb.connect(frame_buffer, snk_framebuffer)
        self.tb.run()

        ref_len = len_frame*3
        det_out = snk_det.data()[:ref_len]
        ref_det = np.concatenate((sym_in1, sym_in2, sym_in1, sym_in2))[:ref_len+1]
        ref_det = np.delete(ref_det, 120)
        self.assertComplexTuplesAlmostEqual(det_out, ref_det, 5)

        costas_out = snk_costas.data()[:ref_len]
        ref_costas = ref_det
        self.assertComplexTuplesAlmostEqual(costas_out, ref_costas, 5)

        preamble_out = snk_preamble.data()[:ref_len]
        ref_preamble = ref_costas
        self.assertComplexTuplesAlmostEqual(preamble_out, ref_preamble, 5)

        framebuffer_out = snk_framebuffer.data()[:ref_len]
        ref_framebuffer = np.concatenate((sym_in2, sym_in1, sym_in2))
        # f, axarr = plt.subplots(3,1)
        # axarr[0].plot(abs(ref_framebuffer - framebuffer_out))
        # axarr[0].set_title('diff abs')
        # axarr[1].plot(np.real(ref_framebuffer))
        # axarr[1].plot(np.imag(ref_framebuffer))
        # axarr[1].set_title('ref')
        # axarr[2].plot(np.real(framebuffer_out))
        # axarr[2].plot(np.imag(framebuffer_out))
        # axarr[2].set_title('framebuffer out')
        # plt.suptitle('framebuffer output')
        # plt.show()

        self.assertComplexTuplesAlmostEqual(framebuffer_out, ref_framebuffer, 5) 


if __name__ == '__main__':
    gr_unittest.run(qa_css_sync)
