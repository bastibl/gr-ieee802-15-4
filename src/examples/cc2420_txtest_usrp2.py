#!/usr/bin/env python

#
# Transmitter of IEEE 802.15.4 RADIO Packets.
#
# Modified by: Thomas Schmid, Sanna Leidelof
#

from gnuradio import gr, eng_notation
from gnuradio import usrp2
from gnuradio import ucla
from gnuradio.ucla_blks import ieee802_15_4_pkt
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import math, struct, time

# insert this in your test code...
import os
print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
raw_input ('Press Enter to continue: ')


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

class transmit_path(gr.top_block):
    def __init__(self, options):
        gr.top_block.__init__(self)

        self.u = usrp2.sink_32fc(options.interface, options.mac_addr)
        self.samples_per_symbol = 2
        self.chan_num = options.channel
        self.data_rate = int (self.u.dac_rate()
                              / self.samples_per_symbol
                              / options.interp_rate)

        self.u.set_center_freq(ieee802_15_4_pkt.chan_802_15_4.chan_map[self.chan_num])
        self.u.set_interp(options.interp_rate)
        if not options.gain:
            g = self.u.gain_range()
            options.gain = float(g[0]+g[1])/2

        self.u.set_gain(options.gain)

        print "cordic_freq = %s" % (eng_notation.num_to_str(ieee802_15_4_pkt.chan_802_15_4.chan_map[self.chan_num]))
        print "data_rate = ", eng_notation.num_to_str(self.data_rate)
        print "samples_per_symbol = ", self.samples_per_symbol
        print "usrp_interp = ", options.interp_rate

        #self.u.set_pga(0, options.gain)
        #self.u.set_pga(1, options.gain)

        # transmitter
        self.packet_transmitter = ieee802_15_4_pkt.ieee802_15_4_mod_pkts(self,
                spb=self.samples_per_symbol, msgq_limit=2)
        self.gain = gr.multiply_const_cc (1)

        self.connect(self.packet_transmitter, self.gain, self.u)

        #self.filesink = gr.file_sink(gr.sizeof_gr_complex, 'tx_test.dat')
        #self.connect(self.gain, self.filesink)

        #self.set_gain(self.subdev.gain_range()[1])  # set max Tx gain
        #self.u.set_auto_tr(True)                      # enable Auto Transmit/Receive switching

    def send_pkt(self, payload='', eof=False):
        return self.packet_transmitter.send_pkt(0xe5, struct.pack("HHHH", 0xFFFF, 0xFFFF, 0x10, 0x10), payload, eof)

def main ():


    parser = OptionParser (option_class=eng_option)
    parser.add_option("-T", "--tx-subdev-spec", type="subdev", default=None,
                      help="select USRP Tx side A or B (default=first one with a daughterboard)")
    parser.add_option ("-c", "--channel", type="eng_float", default=15,
                       help="Set 802.15.4 Channel to listen on", metavar="FREQ")
    parser.add_option ("-i", "--interp_rate", type="int", default=25,
                       help="set interpolation rate")
    parser.add_option ("-r", "--data-rate", type="eng_float", default=2000000)
    parser.add_option ("-g", "--gain", type="eng_float", default=None,
            help="set TX gain. Default: midrange.")
    parser.add_option ("-N", "--no-gui", action="store_true", default=False)
    parser.add_option("-e", "--interface", type="string", default="eth0",
            help="select Ethernet interface, default is eth0")
    parser.add_option("-m", "--mac-addr", type="string", default="",
            help="select USRP by MAC address, default is auto-select")
    parser.add_option("-t", "--msg-interval", type="eng_float", default=1.0,
            help="inter-message interval")

    (options, args) = parser.parse_args ()

    tb = transmit_path(options)
    tb.start()

    i = 0
    while True:
        i+=1
        print "send message %d:"%(i+1,)
        #tb.send_pkt(struct.pack('9B', 0x1, 0x80, 0x80, 0xff, 0xff, 0x10, 0x0, 0x20, 0x0))
        #this is an other example packet we could send.
        tb.send_pkt(struct.pack('BBBBBBBBBBBBBBBBBBBBBBBBBBB', 0x1, 0x8d, 0x8d, 0xff, 0xff, 0xbd, 0x0, 0x22, 0x12, 0xbd, 0x0, 0x1, 0x0, 0xff, 0xff, 0x8e, 0xff, 0xff, 0x0, 0x3, 0x3, 0xbd, 0x0, 0x1, 0x0, 0x0, 0x0))
        time.sleep(options.msg_interval)

    tb.wait()

if __name__ == '__main__':
    # insert this in your test code...
    #import os
    #print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
    #raw_input ('Press Enter to continue: ')

    main ()
