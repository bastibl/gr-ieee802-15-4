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
# This is a multi channel transmitter. It transmits indipendently on
# two different channels of the CC1K. Packet transmitter1 is on the
# higher of the two frequencies, packet transmitter 2 is the lower one.
#
# Modified by: Thomas Schmid
#
  
from gnuradio import gr, eng_notation, optfir
from gnuradio import usrp
from gnuradio import audio
from gnuradio import ucla
from gnuradio.ucla_blks import cc1k_sos_pkt
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import math
import struct, time

#from gnuradio.wxgui import stdgui, fftsink, scopesink
import wx

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

class transmit_path(gr.flow_graph):
    def __init__(self):

        parser = OptionParser (option_class=eng_option)
        parser.add_option("-T", "--tx-subdev-spec", type="subdev", default=None,
                          help="select USRP Tx side A or B (default=first one with a daughterboard)")
        parser.add_option ("-c", "--cordic-freq1", type="eng_float", default=434845200,
                           help="set Tx cordic frequency to FREQ", metavar="FREQ")
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
        self.channel_fs = self.data_rate * self.samples_per_symbol
        self.fs = 4e6
        payload_size = 128             # bytes

        print "data_rate = ", eng_notation.num_to_str(self.data_rate)
        print "samples_per_symbol = ", self.samples_per_symbol
        print "fs = ", eng_notation.num_to_str(self.fs)
        
        gr.flow_graph.__init__(self)
        self.normal_gain = 8000

        self.u = usrp.sink_c()
        dac_rate = self.u.dac_rate();

        self.interp = int(dac_rate / self.fs )
        print "usrp interp = ", self.interp

        self.u.set_interp_rate(self.interp)

        # determine the daughterboard subdevice we're using
        if options.tx_subdev_spec is None:
            options.tx_subdev_spec = usrp.pick_tx_subdevice(self.u)
        self.u.set_mux(usrp.determine_tx_mux_value(self.u, options.tx_subdev_spec))
        self.subdev = usrp.selected_subdev(self.u, options.tx_subdev_spec)
        print "Using TX d'board %s" % (self.subdev.side_and_name(),)

        if options.cordic_freq1 < options.cordic_freq2:
            self.usrp_freq = options.cordic_freq1
            self.freq_diff = options.cordic_freq2 - options.cordic_freq1
        else:
            self.usrp_freq = options.cordic_freq2
            self.freq_diff = options.cordic_freq1 - options.cordic_freq2
        print "freq_diff = ", eng_notation.num_to_str(self.freq_diff)

        self.u.tune(self.subdev._which, self.subdev, self.usrp_freq)
        print "tune USRP to = ", eng_notation.num_to_str(self.usrp_freq)
        self.u.set_pga(0, options.gain)
        self.u.set_pga(1, options.gain)

        interp_factor = int(self.fs / self.channel_fs)
        quad_rate = self.fs
        print "interp_factor = ", interp_factor
        
        # Create filter for the interpolation
        interp_taps = gr.firdes.low_pass (interp_factor,   # gain
                                          self.channel_fs*interp_factor,       # Fs
                                          self.channel_fs/2, # low pass cutoff freq
                                          self.channel_fs*0.1,# width of trans. band
                                          gr.firdes.WIN_HANN) #filter type

        print "len(interp_taps) =", len(interp_taps)

        self.interpolator1 = gr.interp_fir_filter_ccc(interp_factor, interp_taps)
        self.interpolator2 = gr.interp_fir_filter_ccc(interp_factor, interp_taps)

        self.multiplicator = gr.multiply_cc()

        self.adder = gr.add_cc()
        
        self.sin = gr.sig_source_c(self.channel_fs * interp_factor, gr.GR_SIN_WAVE, self.freq_diff, 1, complex(0, 0))

        # transmitter
        self.packet_transmitter1 = cc1k_sos_pkt.cc1k_mod_pkts(self, spb=self.samples_per_symbol, msgq_limit=2)
        #self.packet_transmitter2 = cc1k_sos_pkt.cc1k_mod_pkts(self, spb=self.samples_per_symbol, msgq_limit=2)

        self.amp = gr.multiply_const_cc (self.normal_gain)
        self.filesink = gr.file_sink(gr.sizeof_gr_complex, 'tx_test.dat')
        self.filesink2 = gr.file_sink(gr.sizeof_gr_complex, 'tx_test2.dat')
        self.filesink3 = gr.file_sink(gr.sizeof_gr_complex, 'tx_test3.dat')

        # interpolate the two transmitters
        self.connect(self.packet_transmitter1, self.interpolator1)
        #self.connect(self.packet_transmitter2, self.interpolator2)
        # upconvert the first transmitter)
        self.connect(self.interpolator1, (self.multiplicator, 1))
        self.connect(self.sin, (self.multiplicator, 0))
        # add the two signals
        #self.connect(self.multiplicator, (self.adder, 0))
        #self.connect(self.interpolator2, (self.adder, 1))
        # send the signal to the USRP
        self.connect(self.interpolator1, self.amp, self.filesink)
        self.connect(self.multiplicator, self.filesink2)
        self.connect(self.sin, self.filesink3)
        
        self.set_gain(self.subdev.gain_range()[1])  # set max Tx gain
        self.set_auto_tr(True)                      # enable Auto Transmit/Receive switching

    def set_gain(self, gain):
        self.gain = gain
        self.subdev.set_gain(gain)

    def set_auto_tr(self, enable):
        return self.subdev.set_auto_tr(enable)
        
    def send_pkt1(self, payload='', eof=False):
        return self.packet_transmitter1.send_pkt(am_group=1, module_src=128, module_dst=128, dst_addr=65535, src_addr=2, msg_type=32, payload=payload, eof=eof)
    
    def send_pkt2(self, payload='', eof=False):
        return self.packet_transmitter2.send_pkt(am_group=1, module_src=128, module_dst=128, dst_addr=65535, src_addr=2, msg_type=32, payload=payload, eof=eof)
        
    def bitrate(self):
        return self._bitrate

    def spb(self):
        return self.spb

    def interp(self):
        return self._interp


def main ():
    tx = transmit_path()

    tx.start()

    for i in range(100):
        print "send message %d:"%(i+1,)
        tx.send_pkt1(struct.pack('B', (i+1)%256))
        #tx.send_pkt2(struct.pack('B', (i+1)%256))

        time.sleep(0.05)


    
    tx.wait()

if __name__ == '__main__':
    # insert this in your test code...
    #import os
    #print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
    #raw_input ('Press Enter to continue: ')
    
    main ()
