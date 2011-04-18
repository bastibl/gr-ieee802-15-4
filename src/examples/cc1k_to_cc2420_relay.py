#!/usr/bin/env python

#
# Copyright 2004,2006 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

#
# This test example relays messages from the CC1K to the CC2420.
# The default center frequencies are 434.845MHz for CC1K receive and
# channel 12 (2415MHz) for send.
#
# Modified by: Thomas Schmid
#
  
from gnuradio import gr, eng_notation
from gnuradio import usrp
from gnuradio import ucla
from gnuradio.ucla_blks import ieee802_15_4_pkt
from gnuradio.ucla_blks import cc1k_sos_pkt
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import math, struct, time

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
    """
    This class is used to keep statistics for received
    packets.
    """
    def __init__(self):
        self.npkts = 0
        self.nright = 0

class fsk_rx_graph (gr.flow_graph):
    st = stats()

    def __init__(self, options, rx_callback):
        gr.flow_graph.__init__ (self)

        # ----------------------------------------------------------------

        self.data_rate = 38400
        self.samples_per_symbol = 8
        self.usrp_decim = int (64e6 / self.samples_per_symbol / self.data_rate)
        self.fs = self.data_rate * self.samples_per_symbol
        payload_size = 128             # bytes

        print "data_rate = ", eng_notation.num_to_str(self.data_rate)
        print "samples_per_symbol = ", self.samples_per_symbol
        print "usrp_decim = ", self.usrp_decim
        print "fs = ", eng_notation.num_to_str(self.fs)

        max_deviation = self.data_rate / 4
    
        u = usrp.source_c (0, self.usrp_decim)
        if options.rx_subdev_spec is None:
            options.rx_subdev_spec = pick_subdevice(u)
        u.set_mux(usrp.determine_rx_mux_value(u, options.rx_subdev_spec))

        subdev = usrp.selected_subdev(u, options.rx_subdev_spec)
        print "Using RX d'board %s" % (subdev.side_and_name(),)

        #u.set_rx_freq (0, -options.cordic_freq)
        u.tune(0, subdev, options.cordic_freq_rx)
        u.set_pga(0, options.gain)
        u.set_pga(1, options.gain)


        filter_taps =  gr.firdes.low_pass (1,                   # gain
                                           self.fs,             # sampling rate
                                           self.data_rate / 2 * 1.1, # cutoff
                                           self.data_rate,           # trans width
                                           gr.firdes.WIN_HANN)

        print "len = ", len (filter_taps)

        #filter = gr.fir_filter_ccf (1, filter_taps)

        # receiver
        gain_mu = 0.002*self.samples_per_symbol
        self.packet_receiver = cc1k_sos_pkt.cc1k_demod_pkts(self,
                                                        callback=rx_callback,
                                                        sps=self.samples_per_symbol,
                                                        symbol_rate=self.data_rate,
                                                        p_size=payload_size,
                                                        threshold=-1)

        #filesource = gr.file_source(gr.sizeof_gr_complex, 'tx_test.dat')
        self.connect(u, self.packet_receiver)
            
        #self.filesink = gr.file_sink(gr.sizeof_gr_complex, 'rx_test.dat')
        #self.connect(u, self.filesink)
        
        if 0 and not(options.no_gui):
            fft_input = fftsink.fft_sink_c (self, panel, title="Input", fft_size=512, sample_rate=self.fs)
            self.connect (u, fft_input)
            vbox.Add (fft_input.win, 1, wx.EXPAND)

        #send a packet...

class transmit_path(gr.flow_graph):
    def __init__(self, options):
        gr.flow_graph.__init__(self)
        self.normal_gain = 8000

        self.u = usrp.sink_c()
        dac_rate = self.u.dac_rate();
        self._data_rate = 2000000
        self._spb = 2
        self._interp = int(128e6 / self._spb / self._data_rate)
        self.fs = 128e6 / self._interp

        self.u.set_interp_rate(self._interp)

        # determine the daughterboard subdevice we're using
        if options.tx_subdev_spec is None:
            options.tx_subdev_spec = usrp.pick_tx_subdevice(self.u)
        self.u.set_mux(usrp.determine_tx_mux_value(self.u, options.tx_subdev_spec))
        self.subdev = usrp.selected_subdev(self.u, options.tx_subdev_spec)
        print "Using TX d'board %s" % (self.subdev.side_and_name(),)

        self.u.tune(self.subdev._which, self.subdev, options.cordic_freq_tx)
        self.u.set_pga(0, options.gain)
        self.u.set_pga(1, options.gain)

        # transmitter
        self.packet_transmitter = ieee802_15_4_pkt.ieee802_15_4_mod_pkts(self, spb=self._spb, msgq_limit=2)
        self.gain = gr.multiply_const_cc (self.normal_gain)
        
        self.connect(self.packet_transmitter, self.gain, self.u)

        self.set_gain(self.subdev.gain_range()[1])  # set max Tx gain
        self.set_auto_tr(True)                      # enable Auto Transmit/Receive switching

    def set_gain(self, gain):
        self.gain = gain
        self.subdev.set_gain(gain)

    def set_auto_tr(self, enable):
        return self.subdev.set_auto_tr(enable)
        
    def send_pkt(self, payload='', eof=False):
        """
        Send a packet with a predetermined sequence number and from/to address.
        """
        return self.packet_transmitter.send_pkt(0xe5, struct.pack("HHHH", 0xFFFF, 0xFFFF, 0x10, 0x10), payload, eof)

    def send_pkt(self, seqno, address, payload='', eof=False):
        return self.packet_transmitter.send_pkt(seqno, address, payload, eof)

def main ():

        
    def rx_callback(ok, am_group, src_addr, dst_addr, module_src, module_dst, msg_type, payload, crc):
        st.npkts += 1
        if ok:
            st.nright += 1
            #we have to fake this since it doesn't exist in cc1k
            pktno = st.nright % 256

            print "ok = %5r  pktno = %4d  len(payload) = %4d  %d/%d" % (ok, pktno, len(payload),
                                                                        st.nright, st.npkts)
            print "  payload: " + str(map(hex, map(ord, payload)))

            addressInfo = struct.pack("HH", dst_addr, src_addr)
            sosHdr = chr(module_dst)+chr(module_src)+chr(msg_type)
            print "\nRetransmit "
            fgtx.send_pkt(pktno, chr(0)+addressInfo, ''.join((sosHdr, payload)))
            print " ------------------------"


    parser = OptionParser (option_class=eng_option)
    parser.add_option("-R", "--rx-subdev-spec", type="subdev", default=None,
                      help="select USRP Rx side A or B (default=first one with a daughterboard)")
    parser.add_option("-T", "--tx-subdev-spec", type="subdev", default=None,
                      help="select USRP Tx side A or B (default=first one with a daughterboard)")

    parser.add_option ("-t", "--cordic-freq-tx", type="eng_float", default=2415000000,
                       help="set Tx cordic frequency to FREQ", metavar="FREQ")

    parser.add_option ("-c", "--cordic-freq-rx", type="eng_float", default=434845200,
                       help="set rx cordic frequency to FREQ", metavar="FREQ")
    parser.add_option ("-r", "--data-rate", type="eng_float", default=2000000)
    parser.add_option ("-f", "--filename", type="string",
                       default="rx.dat", help="write data to FILENAME")
    parser.add_option ("-g", "--gain", type="eng_float", default=0,
                       help="set Rx PGA gain in dB [0,20]")
    parser.add_option ("-N", "--no-gui", action="store_true", default=False)
    
    (options, args) = parser.parse_args ()

    print "cordic_freq_rx = %s" % (eng_notation.num_to_str (options.cordic_freq_rx))
    print "cordic_freq_tx = %s" % (eng_notation.num_to_str (options.cordic_freq_tx))
        
    st = stats()

    fgtx = transmit_path(options)
    fgtx.start()

    fgrx = fsk_rx_graph(options, rx_callback)
    fgrx.start()

    fgrx.wait()
    fgtx.wait()
    

if __name__ == '__main__':
    # insert this in your test code...
    #import os
    #print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
    #raw_input ('Press Enter to continue: ')
    
    main ()
