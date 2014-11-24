#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 <+YOU OR YOUR COMPANY+>.
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
import matplotlib.pyplot as plt

class qa_rayleigh_multipath_cc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # set up fg
        data_in = np.ones((100000,))
        self.src = blocks.vector_source_c(data_in)
        self.rayleigh = ieee802_15_4.rayleigh_multipath_cc(np.ones((10,)),10)
        self.snk = blocks.vector_sink_c(1)
        self.tb.connect(self.src, self.rayleigh, self.snk)
        self.tb.run ()
        # check data
        e_in =  sum(np.array(abs(np.array(data_in))**2))/len(data_in)
        e_out = sum(np.array(abs(np.array(self.snk.data()))**2))/len(self.snk.data())
        print "power of output signal: ", e_out
        print "power of input signal: ", e_in
        # plt.plot(abs(np.array(self.rayleigh.taps()))**2)
        # plt.show()
        self.assertTrue(e_out-e_in < 1e-2);


if __name__ == '__main__':
    gr_unittest.run(qa_rayleigh_multipath_cc)
