#!/usr/bin/env python

#
#
# Modified by: Thomas Schmid
#
  
from gnuradio import gr, eng_notation
from gnuradio import usrp
from gnuradio import audio
from gnuradio import ucla
from gnuradio.ucla_blks import cc1k_sos_pkt
from gnuradio.ucla_blks import ieee802_15_4_pkt
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import math, sys
import struct, time

class transmit_path(gr.flow_graph):
    """ This class implements the send path for the CC1K.
    """
    def __init__(self):
        gr.flow_graph.__init__(self)

        self.u = usrp.sink_c()

    def configure_cc1k(self):
        #self.disconnect_all()
        cordic_freq = 434845200
        data_rate = 38400
        gain=0

        print "cordic_freq = %s" % (eng_notation.num_to_str (cordic_freq))

        self.data_rate = data_rate
        self.samples_per_symbol = 8
        self.fs = self.data_rate * self.samples_per_symbol
        payload_size = 128             # bytes

        print "data_rate = ", eng_notation.num_to_str(self.data_rate)
        print "samples_per_symbol = ", self.samples_per_symbol
        print "fs = ", eng_notation.num_to_str(self.fs)

        self.normal_gain = 8000

        dac_rate = self.u.dac_rate();

        self.interp = int(128e6 / self.samples_per_symbol / self.data_rate)
        print "usrp interp = ", self.interp
        self.fs = 128e6 / self.interp

        self.u.set_interp_rate(self.interp)

        # determine the daughterboard subdevice we're using
        self.u.set_mux(usrp.determine_tx_mux_value(self.u, (1, 0)))
        self.subdev = usrp.selected_subdev(self.u, (1, 0))
        print "Using TX d'board %s" % (self.subdev.side_and_name(),)

        self.u.tune(self.subdev._which, self.subdev, cordic_freq)
        self.u.set_pga(0, gain)
        self.u.set_pga(1, gain)

        # transmitter
        self.packet_transmitter = cc1k_sos_pkt.cc1k_mod_pkts(self, spb=self.samples_per_symbol, msgq_limit=2)
        self.amp = gr.multiply_const_cc (self.normal_gain)

        self.connect(self.packet_transmitter, self.amp, self.u)

        self.set_gain(self.subdev.gain_range()[1])  # set max Tx gain
        self.set_auto_tr(True)                      # enable Auto Transmit/Receive switching

    def set_gain(self, gain):
        self.gain = gain
        self.subdev.set_gain(gain)

    def set_auto_tr(self, enable):
        return self.subdev.set_auto_tr(enable)
        
    def send_pkt_cc1k(self, payload='', eof=False):
        return self.packet_transmitter.send_pkt(am_group=1, module_src=128, module_dst=128, dst_addr=65535, src_addr=2, msg_type=32, payload=payload, eof=eof)
        
    def bitrate(self):
        return self._bitrate

    def spb(self):
        return self.spb

    def interp(self):
        return self._interp


##########################################################
    
    def configure_cc2420(self):
        self.disconnect_all()
        gain = 0
        cordic_freq = 2415000000
        self.normal_gain = 8000

        dac_rate = self.u.dac_rate();
        self._data_rate = 2000000
        self._spb = 2
        self._interp = int(128e6 / self._spb / self._data_rate)
        self.fs = 128e6 / self._interp

        self.u.set_interp_rate(self._interp)

        # determine the daughterboard subdevice we're using
        self.u.set_mux(usrp.determine_tx_mux_value(self.u, (0, 0)))
        self.subdev = usrp.selected_subdev(self.u, (0, 0))
        print "Using TX d'board %s" % (self.subdev.side_and_name(),)

        self.u.tune(self.subdev._which, self.subdev, cordic_freq)
        self.u.set_pga(0, gain)
        self.u.set_pga(1, gain)

        # transmitter
        self.packet_transmitter = ieee802_15_4_pkt.ieee802_15_4_mod_pkts(self, spb=self._spb, msgq_limit=2)
        self.gain = gr.multiply_const_cc (self.normal_gain)
        
        self.connect(self.packet_transmitter, self.gain, self.u)

        #self.filesink = gr.file_sink(gr.sizeof_gr_complex, 'rx_test.dat')
        #self.connect(self.gain, self.filesink)

        self.set_gain(self.subdev.gain_range()[1])  # set max Tx gain
        self.set_auto_tr(True)                      # enable Auto Transmit/Receive switching

    def send_pkt_cc2420(self, payload='', eof=False):
        return self.packet_transmitter.send_pkt(0xe5, struct.pack("HHHH", 0xFFFF, 0xFFFF, 0x10, 0x10), payload, eof)


def main():
    

    tx = transmit_path()
    tx.configure_cc1k()
    
    tx.start()
    for i in range(2):
        print "send cc1k message %d:"%(i+1,)
        tx.send_pkt_cc1k(struct.pack('B', (i+1)%256))

        time.sleep(1)
    print "end"

    tx.stop()
    tx.configure_cc2420()
    tx.start()
    print "send_cc2420"

    for i in range(2):
        print "send cc2420 message %d:"%(i+1,)
        tx.send_pkt_cc2420(struct.pack('9B', 0x1, 0x80, 0x80, 0xff, 0xff, 0x10, 0x0, 0x20, 0x0))
        time.sleep(1)
        
    tx.stop()
    
if __name__ == '__main__':
    # insert this in your test code...
    #import os
    #print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
    #raw_input ('Press Enter to continue: ')
    
    main ()
