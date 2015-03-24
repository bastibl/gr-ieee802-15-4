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
import ieee802_15_4_swig as ieee802_15_4
import numpy as np

class qa_costas_loop_cc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self): # perfect sync, known start
        # set up fg
        self.tb.run ()
        nsym = 1000
        data_in = 2*(np.random.randint(0,2,nsym)-0.5) + 2j*(np.random.randint(0,2,nsym)-0.5) # stream of random qpsk symbols
        data_in[0] = 1+1j
        src = blocks.vector_source_c(data_in)
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), 0)
        snk = blocks.vector_sink_c()
        self.tb.connect(src, costas, snk)
        self.tb.run()
        # check data
        data_out = snk.data()
        self.assertComplexTuplesAlmostEqual(np.angle(data_in), np.angle(data_out))

    def test_002_t (self): # perfect sync, random start
        # set up fg
        self.tb.run ()
        nsym = 1000
        data_in = 2*(np.random.randint(0,2,nsym)-0.5) + 2j*(np.random.randint(0,2,nsym)-0.5) # stream of random qpsk symbols
        src = blocks.vector_source_c(data_in)
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), -1)
        snk = blocks.vector_sink_c()
        self.tb.connect(src, costas, snk)
        self.tb.run()
        # check data
        data_out = snk.data()
        self.assertComplexTuplesAlmostEqual(np.angle(data_in), np.angle(data_out))

    def test_003_t (self): # phase offset
        # set up fg
        self.tb.run ()
        nsym = 1000
        phi_off = np.pi*0.2
        data_in = 2*(np.random.randint(0,2,nsym)-0.5) + 2j*(np.random.randint(0,2,nsym)-0.5) # stream of random qpsk symbols
        data_in[0] = 1+1j
        data_in_off = data_in*np.exp(1j*phi_off)
        src = blocks.vector_source_c(data_in_off)
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), 0)
        snk = blocks.vector_sink_c()
        self.tb.connect(src, costas, snk)
        self.tb.run()
        # check data
        data_out = snk.data()
        self.assertComplexTuplesAlmostEqual(np.angle(data_in), np.angle(data_out))

    def test_004_t (self): # phase offset, lock to "wrong" symbol
        # set up fg
        self.tb.run ()
        nsym = 1000
        phi_off = np.pi*0.4
        data_in = 2*(np.random.randint(0,2,nsym)-0.5) + 2j*(np.random.randint(0,2,nsym)-0.5) # stream of random qpsk symbols
        data_in[0] = 1+1j
        data_in_off = data_in*np.exp(1j*phi_off)
        src = blocks.vector_source_c(data_in_off)
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), 0)
        snk = blocks.vector_sink_c()
        self.tb.connect(src, costas, snk)
        self.tb.run()
        # check data
        data_out = snk.data()
        self.assertComplexTuplesAlmostEqual(np.angle(data_in*np.exp(1j*np.pi/2)), np.angle(data_out))

    def test_005_t (self): # frequency offset
        # set up fg
        self.tb.run ()
        nsym = 1000
        phi_off = np.arange(nsym)*np.pi/7
        data_in = 2*(np.random.randint(0,2,nsym)-0.5) + 2j*(np.random.randint(0,2,nsym)-0.5) # stream of random qpsk symbols
        data_in[0] = 1+1j
        data_in_off = data_in*np.exp(1j*phi_off)
        src = blocks.vector_source_c(data_in_off)
        costas = ieee802_15_4.costas_loop_cc((1+1j, -1+1j, -1-1j, 1-1j), 0)
        snk = blocks.vector_sink_c()
        self.tb.connect(src, costas, snk)
        self.tb.run()
        # check data
        data_out = snk.data()
        self.assertComplexTuplesAlmostEqual(np.angle(data_in), np.angle(data_out))


if __name__ == '__main__':
    gr_unittest.run(qa_costas_loop_cc)
