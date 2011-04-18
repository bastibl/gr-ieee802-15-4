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
# This test example relays messages from one frequency to an other.
# The default center frequencies are Channel 11 for receive and
# channel 25 for send.
#
# Modified by: Thomas Schmid
#
  
from gnuradio import gr, eng_notation
from gnuradio import usrp
from gnuradio import ucla
from gnuradio.ucla_blks import ieee802_15_4_pkt
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

class oqpsk_rx_graph (gr.flow_graph):
    """
    This class connects the USRP source with the
    IEEE 802.15.4 packet receiver. It needs a callback function
    which will be called every time a packet is successfully
    decoded. There is no check of any CRC done in here.

    """
    
    def __init__(self, options, rx_callback):
        """
        @param options Optparse option field for command line arguments.
        @param rx_callback Callback function for the event when a packet is received.
        """
        gr.flow_graph.__init__(self)
        print "cordic_freq = %s" % (eng_notation.num_to_str (options.cordic_freq_rx))


        # ----------------------------------------------------------------

        self.data_rate = options.data_rate
        self.samples_per_symbol = 2
        self.usrp_decim = int (64e6 / self.samples_per_symbol / self.data_rate)
        self.fs = self.data_rate * self.samples_per_symbol
        payload_size = 128             # bytes

        print "data_rate = ", eng_notation.num_to_str(self.data_rate)
        print "samples_per_symbol = ", self.samples_per_symbol
        print "usrp_decim = ", self.usrp_decim
        print "fs = ", eng_notation.num_to_str(self.fs)

        u = usrp.source_c (0, self.usrp_decim)
        if options.rx_subdev_spec is None:
            options.rx_subdev_spec = pick_subdevice(u)
        u.set_mux(usrp.determine_rx_mux_value(u, options.rx_subdev_spec))

        self.subdev = usrp.selected_subdev(u, options.rx_subdev_spec)
        print "Using RX d'board %s" % (self.subdev.side_and_name(),)
        #self.subdev.select_rx_antenna('RX2')

        u.tune(0, self.subdev, options.cordic_freq_rx)
        u.set_pga(0, options.gain)
        u.set_pga(1, options.gain)

        self.u = u

        self.packet_receiver = ieee802_15_4_pkt.ieee802_15_4_demod_pkts(self,
                                                                callback=rx_callback,
                                                                sps=self.samples_per_symbol,
                                                                symbol_rate=self.data_rate,
                                                                threshold=-1)

        self.squelch = gr.pwr_squelch_cc(50, 1, 0, True)
        #self.file_sink = gr.file_sink(gr.sizeof_gr_complex, "/dev/null")
        self.connect(self.u, self.squelch, self.packet_receiver)
        #self.connect(self.u, self.file_sink)
        
        self.set_auto_tr(True)                      # enable Auto Transmit/Receive switching

    def set_auto_tr(self, enable):
        return self.subdev.set_auto_tr(enable)

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

        
    def rx_callback(ok, payload):
        st.npkts += 1
        if ok:
            st.nright += 1
            (pktno,) = struct.unpack('!B', payload[2:3])
            print "ok = %5r  pktno = %4d  len(payload) = %4d  %d/%d" % (ok, pktno, len(payload),
                                                                        st.nright, st.npkts)
            print "  payload: " + str(map(hex, map(ord, payload)))

            print "\nRetransmit"
            fgtx.send_pkt(pktno, payload[3:11], payload[11:len(payload)-2])
            print " ------------------------"


    parser = OptionParser (option_class=eng_option)
    parser.add_option("-R", "--rx-subdev-spec", type="subdev", default=None,
                      help="select USRP Rx side A or B (default=first one with a daughterboard)")
    parser.add_option("-T", "--tx-subdev-spec", type="subdev", default=None,
                      help="select USRP Tx side A or B (default=first one with a daughterboard)")
    parser.add_option ("-t", "--cordic-freq-tx", type="eng_float", default=2415000000,
                       help="set Tx cordic frequency to FREQ", metavar="FREQ")
    parser.add_option ("-c", "--cordic-freq-rx", type="eng_float", default=2405000000,
                       help="set rx cordic frequency to FREQ", metavar="FREQ")
    parser.add_option ("-r", "--data-rate", type="eng_float", default=2000000)
    parser.add_option ("-f", "--filename", type="string",
                       default="rx.dat", help="write data to FILENAME")
    parser.add_option ("-g", "--gain", type="eng_float", default=0,
                       help="set Rx PGA gain in dB [0,20]")
    parser.add_option ("-N", "--no-gui", action="store_true", default=False)
    
    (options, args) = parser.parse_args ()

    st = stats()

    fgtx = transmit_path(options)
    fgtx.start()

    fgrx = oqpsk_rx_graph(options, rx_callback)
    fgrx.start()

    fgrx.wait()
    fgtx.wait()
    

if __name__ == '__main__':
    # insert this in your test code...
    #import os
    #print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
    #raw_input ('Press Enter to continue: ')
    
    main ()
