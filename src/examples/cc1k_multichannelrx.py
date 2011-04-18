#!/usr/bin/env python

#
# Copyright (c) 2006 The Regents of the University of California.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
# 3. Neither the name of the University nor that of the Laboratory
#    may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


#
# Decoder of Mica2 RADIO Packets. We use the SOS operating system for Mica2s.
# Similar code should also work with TinyOS, though you would want to modify
# the packet structure in cc1k_sos_pkt.py. This demo will demodulate two
# mica2 channels simultaniously.
#
# Modified by: Thomas Schmid
#
  
from gnuradio import gr, eng_notation
from gnuradio import usrp
from gnuradio import audio
from gnuradio import ucla
from gnuradio.ucla_blks import cc1k_sos_pkt
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import math

#from gnuradio.wxgui import stdgui, fftsink, scopesink
#import wx

def pick_subdevice(u):
    """
    The user didn't specify a subdevice on the command line.
    If there's a daughterboard on A, select A.
    If there's a daughterboard on B, select B.
    Otherwise, select A.
    """
    if u.db[0][0].dbid() >= 0:       # dbid is < 0 if there's no d'board or a problem
        return (0, 0)
    if u.db[1][0].dbid() >= 0:
        return (1, 0)
    return (0, 0)

class stats(object):
    def __init__(self):
        self.npkts = 0
        self.nright = 0
        
    
class fsk_rx_graph (gr.flow_graph):
    st1 = stats()
    st2 = stats()

    def __init__(self):
        gr.flow_graph.__init__ (self)

        parser = OptionParser (option_class=eng_option)
        parser.add_option("-R", "--rx-subdev-spec", type="subdev", default=None,
                          help="select USRP Rx side A or B (default=first one with a daughterboard)")
        parser.add_option ("-c", "--cordic-freq1", type="eng_float", default=434845200,
                           help="set rx cordic frequency for channel 1 to FREQ", metavar="FREQ")
        parser.add_option ("-d", "--cordic-freq2", type="eng_float", default=434318512,
                           help="set rx cordic frequency for channel 2 to FREQ", metavar="FREQ")
        parser.add_option ("-g", "--gain", type="eng_float", default=0,
                           help="set Rx PGA gain in dB [0,20]")
        (options, args) = parser.parse_args ()
        print "cordic_freq1 = %s" % (eng_notation.num_to_str (options.cordic_freq1))
        print "cordic_freq2 = %s" % (eng_notation.num_to_str (options.cordic_freq2))

        # ----------------------------------------------------------------

        self.data_rate = 38400
        self.samples_per_symbol = 8
        #we sample a band of 4 MHz.
        self.usrp_decim = int (64e6 / 4e6)
        self.decimation = self.usrp_decim / self.samples_per_symbol / self.data_rate
        
        self.fs = self.data_rate * self.samples_per_symbol
        payload_size = 128             # bytes

        print "data_rate = ", eng_notation.num_to_str(self.data_rate)
        print "samples_per_symbol = ", self.samples_per_symbol
        print "usrp_decim = ", self.usrp_decim
        print "decimation = ", self.decimation
        print "fs = ", eng_notation.num_to_str(self.fs)


        if options.cordic_freq1 < options.cordic_freq2:
            self.usrp_freq = options.cordic_freq1
            self.freq_diff = options.cordic_freq1 - options.cordic_freq2
        else:
            self.usrp_freq = options.cordic_freq2
            self.freq_diff = options.cordic_freq2 - options.cordic_freq1

        print "tune USRP to = ", self.usrp_freq
        u = usrp.source_c (0, self.usrp_decim)
        if options.rx_subdev_spec is None:
            options.rx_subdev_spec = pick_subdevice(u)
        u.set_mux(usrp.determine_rx_mux_value(u, options.rx_subdev_spec))

        subdev = usrp.selected_subdev(u, options.rx_subdev_spec)
        print "Using RX d'board %s" % (subdev.side_and_name(),)

        #u.set_rx_freq (0, -options.cordic_freq)
        u.tune(0, subdev, self.usrp_freq)
        u.set_pga(0, options.gain)
        u.set_pga(1, options.gain)

        # Create filter to get actual channels we want
        chan_coeffs = gr.firdes.low_pass (1.0,                # gain
                                          4e6,                # sampling rate
                                          150e3,              # low pass cutoff freq
                                          50e3,                # width of trans. band
                                          gr.firdes.WIN_HANN) # filter type 

        print "len(rx_chan_coeffs) =", len(chan_coeffs)

        # Decimating Channel filter with frequency translation
        # complex in and out, float taps
        self.ddc1 = gr.freq_xlating_fir_filter_ccf(13,       # decimation rate
                                                   chan_coeffs,    # taps
                                                   0,              # frequency translation amount
                                                   4e6)   # input sample rate

        self.ddc2 = gr.freq_xlating_fir_filter_ccf(13,       # decimation rate
                                                   chan_coeffs,    # taps
                                                   self.freq_diff,              # frequency translation amount
                                                   4e6)   # input sample rate


        # receiver
        gain_mu = 0.002*self.samples_per_symbol
        self.packet_receiver1 = cc1k_sos_pkt.cc1k_demod_pkts(self,
                                                        callback=self.rx_callback1,
                                                        sps=self.samples_per_symbol,
                                                        symbol_rate=self.data_rate,
                                                        p_size=payload_size,
                                                        threshold=-1)
        self.packet_receiver2 = cc1k_sos_pkt.cc1k_demod_pkts(self,
                                                        callback=self.rx_callback2,
                                                        sps=self.samples_per_symbol,
                                                        symbol_rate=self.data_rate,
                                                        p_size=payload_size,
                                                        threshold=-1)


        u = gr.file_source(gr.sizeof_gr_complex, 'tx_test.dat')
        self.connect(u, self.ddc1, self.packet_receiver1)
        self.connect(u, self.ddc2, self.packet_receiver2)
        
            
        self.filesink = gr.file_sink(gr.sizeof_gr_complex, 'rx_test.dat')
        #self.connect(u, self.filesink)
        
        if 0 and not(options.no_gui):
            fft_input = fftsink.fft_sink_c (self, panel, title="Input", fft_size=512, sample_rate=self.fs)
            self.connect (u, fft_input)
            vbox.Add (fft_input.win, 1, wx.EXPAND)

        #send a packet...


    def rx_callback1(self, ok, am_group, src_addr, dst_addr, module_src, module_dst, msg_type, msg_payload, crc):
        self.st1.npkts += 1
        if ok:
            self.st1.nright += 1

        print " ------------------------"
        print "ok = %5r  %d/%d total %d" % (ok, self.st1.nright, self.st1.npkts, self.st1.npkts+self.st2.npkts)
        print " am group: " + str(am_group)
        print "  src_addr: "+str(src_addr)+" dst_addr: "+str(dst_addr)
        print "  src_module: " + str(module_src) + " dst_module: " + str(module_dst)
        print "  msg type: " + str(msg_type)
        print "  msg: " + str(map(hex, map(ord, msg_payload)))
        print "  crc: " + str(crc)
        print " ------------------------"

    def rx_callback2(self, ok, am_group, src_addr, dst_addr, module_src, module_dst, msg_type, msg_payload, crc):
        self.st2.npkts += 1
        if ok:
            self.st2.nright += 1
        n = 30
        print n*" " + " ++++++++++++++++++++++++"
        print n*" " + "ok = %5r  %d/%d total %d" % (ok, self.st2.nright, self.st2.npkts, self.st1.npkts+self.st2.npkts)
        print n*" " + " am group: " + str(am_group)
        print n*" " + "  src_addr: "+str(src_addr)+" dst_addr: "+str(dst_addr)
        print n*" " + "  src_module: " + str(module_src) + " dst_module: " + str(module_dst)
        print n*" " + "  msg type: " + str(msg_type)
        print n*" " + "  msg: " + str(map(hex, map(ord, msg_payload)))
        print n*" " + "  crc: " + str(crc)
        print n*" " + " ++++++++++++++++++++++++"


def main ():
    #tx = transmit_path()
    rx = fsk_rx_graph()
    rx.start()
    rx.wait()

if __name__ == '__main__':
    # insert this in your test code...
    #import os
    #print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
    #raw_input ('Press Enter to continue: ')
    
    main ()
