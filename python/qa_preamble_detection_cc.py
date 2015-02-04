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
import ieee802_15_4_swig as ieee802_15_4
import numpy as np

class qa_preamble_detection_cc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self): # no phase offset
        # set up fg
        preamble = (1+1j)*np.ones((32,))
        rand = np.random.randint(-1,2,3200)
        data = (1-1j)*np.ones((3200,))*rand
        data_in = np.concatenate((preamble, np.transpose(data)))
        src = blocks.vector_source_c(data_in)
        det = ieee802_15_4.preamble_detection_cc(len(preamble), preamble[0])
        snk = blocks.vector_sink_c()
        self.tb.connect(src, det, snk)
        self.tb.run ()
        # check data
        data_out = snk.data()
        self.assertComplexTuplesAlmostEqual(data_out, data_in)

    def test_002_t (self): # with phase offset
        # set up fg
        preamble = (1+1j)*np.ones((32,))
        rand = np.random.randint(-1,2,3200)
        data = (1-1j)*np.ones((3200,))*rand
        data_in = np.concatenate((preamble, np.transpose(data)))
        phi_off = np.pi/4
        data_in *= np.exp(1j*phi_off)
        src = blocks.vector_source_c(data_in)
        det = ieee802_15_4.preamble_detection_cc(len(preamble), preamble[0])
        snk = blocks.vector_sink_c()
        self.tb.connect(src, det, snk)
        self.tb.run ()
        # check data
        data_out = snk.data()
        self.assertComplexTuplesAlmostEqual(data_out, data_in*np.exp(-1j*phi_off), 5)

if __name__ == '__main__':
    gr_unittest.run(qa_preamble_detection_cc)
