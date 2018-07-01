#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 Felix Wunsch, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT) <wunsch.felix@googlemail.com>.
# Portions copyright 2018 Spukhafte Systems Limited
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
import numpy as np
import time
import ieee802_15_4_swig as ieee802_15_4

class qa_pn9_whitener (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # set up flowgraph
        data = bytearray(512)
        self.src = blocks.vector_source_b(data, False, 1, [])
        self.s2ts = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 512, "packet_len")
        self.ts2pdu = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")
        self.pn9 = ieee802_15_4.pn9_whitener(0xFFFF)
        self.pdu2ts = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        self.snk = blocks.vector_sink_b(1)

        self.tb.connect(self.src, self.s2ts, self.ts2pdu)
        self.tb.msg_connect(self.ts2pdu, "pdus", self.pn9, "in")
        self.tb.msg_connect(self.pn9, "out", self.pdu2ts, "pdus")
        self.tb.connect(self.pdu2ts, self.snk)

        self.tb.start()
        time.sleep(1)
        self.tb.stop()

        # check data
        data_out = self.snk.data()
        #print "output:"
        #print data_out

        expected_output = (240, 14, 205, 246, 194, 25, 18, 117, 61, 233, 28, 184, 203, 43, 5, 170,
                           190, 22, 236, 182, 6, 221, 199, 179, 172, 99, 209, 95, 26, 101, 12, 152,
                           169, 201, 111, 73, 246, 211, 10, 69, 110, 122, 195, 42, 39, 140, 16, 32,
                           98, 226, 106, 227, 72, 197, 230, 243, 104, 167, 4, 153, 139, 239, 193,
                           127, 120, 135, 102, 123, 225, 12, 137, 186, 158, 116, 14, 220, 229, 149,
                           2, 85, 95, 11, 118, 91, 131, 238, 227, 89, 214, 177, 232, 47, 141, 50,
                           6, 204, 212, 228, 183, 36, 251, 105, 133, 34, 55, 189, 97, 149, 19, 70,
                           8, 16, 49, 113, 181, 113, 164, 98, 243, 121, 180, 83, 130, 204, 197,
                           247, 224, 63, 188, 67, 179, 189, 112, 134, 68, 93, 79, 58, 7, 238, 242,
                           74, 129, 170, 175, 5, 187, 173, 65, 247, 241, 44, 235, 88, 244, 151, 70,
                           25, 3, 102, 106, 242, 91, 146, 253, 180, 66, 145, 155, 222, 176, 202, 9,
                           35, 4, 136, 152, 184, 218, 56, 82, 177, 249, 60, 218, 41, 65, 230, 226,
                           123, 240, 31, 222, 161, 217, 94, 56, 67, 162, 174, 39, 157, 3, 119, 121,
                           165, 64, 213, 215, 130, 221, 214, 160, 251, 120, 150, 117, 44, 250, 75,
                           163, 140, 1, 51, 53, 249, 45, 201, 126, 90, 161, 200, 77, 111, 88, 229,
                           132, 17, 2, 68, 76, 92, 109, 28, 169, 216, 124, 30, 237, 148, 32, 115,
                           241, 61, 248, 15, 239, 208, 108, 47, 156, 33, 81, 215, 147, 206, 129,
                           187, 188, 82, 160, 234, 107, 193, 110, 107, 208, 125, 60, 203, 58, 22,
                           253, 165, 81, 198, 128, 153, 154, 252, 150, 100, 63, 173, 80, 228, 166,
                           55, 172, 114, 194, 8, 1, 34, 38, 174, 54, 142, 84, 108, 62, 143, 118,
                           74, 144, 185, 248, 30, 252, 135, 119, 104, 182, 23, 206, 144, 168, 235,
                           73, 231, 192, 93, 94, 41, 80, 245, 181, 96, 183, 53, 232, 62, 158, 101,
                           29, 139, 254, 210, 40, 99, 192, 76, 77, 126, 75, 178, 159, 86, 40, 114,
                           211, 27, 86, 57, 97, 132, 0, 17, 19, 87, 27, 71, 42, 54, 159, 71, 59,
                           37, 200, 92, 124, 15, 254, 195, 59, 52, 219, 11, 103, 72, 212, 245, 164,
                           115, 224, 46, 175, 20, 168, 250, 90, 176, 219, 26, 116, 31, 207, 178,
                           142, 69, 127, 105, 148, 49, 96, 166, 38, 191, 37, 217, 79, 43, 20, 185,
                           233, 13, 171, 156, 48, 66, 128, 136, 137, 171, 141, 35, 21, 155, 207,
                           163, 157, 18, 100, 46, 190, 7, 255, 225, 29, 154, 237, 133, 51, 36, 234,
                           122, 210, 57, 112, 151, 87, 10, 84, 125, 45, 216, 109, 13, 186, 143,
                           103, 89, 199, 162, 191, 52, 202, 24, 48, 83, 147, 223, 146, 236, 167,
                           21, 138, 220, 244, 134, 85, 78, 24, 33, 64, 196, 196, 213, 198, 145,
                           138, 205, 231, 209, 78, 9, 50, 23, 223, 131, 255, 240)
        self.assertEqual(data_out, expected_output)

if __name__ == '__main__':
    gr_unittest.run(qa_pn9_whitener, "qa_pn9_whitener.xml")
