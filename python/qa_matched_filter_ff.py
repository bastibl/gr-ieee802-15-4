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

class qa_matched_filter_ff (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # set up fg
        self.src = blocks.vector_source_f((1,2,1,0,-1,0))
        self.mf = ieee802_15_4.matched_filter_ff((1,3,1))
        self.snk = blocks.vector_sink_f(1)
        self.tb.connect(self.src, self.mf, self.snk)
        self.tb.run ()
        # check data
        data = self.snk.data()
        ref = (8,-3)
        print data
        self.assertFloatTuplesAlmostEqual(data, ref)

if __name__ == '__main__':
    gr_unittest.run(qa_matched_filter_ff)
