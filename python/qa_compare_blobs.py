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
import pmt
import time
import numpy as np

class qa_compare_blobs (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    # def test_001_t (self):
    #     # set up fg
    #     self.trigger = blocks.message_strobe(pmt.cons(pmt.intern("trigger"), pmt.intern("dummycdr")),10)
    #     self.src_ref = ieee802_15_4.make_pair_with_blob((np.uint8(0), np.uint8(1), np.uint8(2), np.uint8(3)))
    #     self.src_test = ieee802_15_4.make_pair_with_blob((np.uint8(1), np.uint8(1), np.uint8(2), np.uint8(3)))
    #     self.snk = ieee802_15_4.compare_blobs()
    #     self.tb.msg_connect(self.trigger, "strobe", self.src_ref, "in")
    #     self.tb.msg_connect(self.trigger, "strobe", self.src_test, "in")
    #     self.tb.msg_connect(self.src_ref, "out", self.snk, "ref")
    #     self.tb.msg_connect(self.src_test, "out", self.snk, "test")
    #     self.tb.start()
    #     time.sleep(0.1)
    #     self.tb.stop()
    #     # check data
    #     bits_per_blob = 4*8
    #     errors_per_blob = 2.0
    #     ref_ber = errors_per_blob/bits_per_blob
    #     ber = self.snk.get_ber()
    #     print "ber: ", ber
    #     print "ref ber:", ref_ber
    #     self.assertTrue(ref_ber == ber)

if __name__ == '__main__':
    gr_unittest.run(qa_compare_blobs)
