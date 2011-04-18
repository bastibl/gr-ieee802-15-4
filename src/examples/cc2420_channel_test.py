#!/usr/bin/env python

#
# This test example tests the code over a simulated channel.
#
# Modified by: Thomas Schmid
#
  
from gnuradio import gr, eng_notation
from gnuradio import ucla
from gnuradio.ucla_blks import ieee802_15_4_pkt
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import math, struct, time

class stats(object):
    """
    This class is used to keep statistics for received
    packets.
    """
    def __init__(self):
        self.npkts = 0
        self.nright = 0

class my_graph (gr.flow_graph):
    """
    """
    
    def __init__(self, rx_callback, SNR):
        """
        @param options Optparse option field for command line arguments.
        @param rx_callback Callback function for the event when a packet is received.
        """
        gr.flow_graph.__init__(self)

        self.samples_per_symbol = 2
	self.data_rate = 2000000
        payload_size = 128             # bytes

	self.packet_transmitter = ieee802_15_4_pkt.ieee802_15_4_mod_pkts(self, spb=self.samples_per_symbol, msgq_limit=2)

        # add some noise
	print " Setting SNR to ", SNR
        add = gr.add_cc()
        noise = gr.noise_source_c(gr.GR_GAUSSIAN, pow(10.0,-SNR/20.0))

        self.packet_receiver = ieee802_15_4_pkt.ieee802_15_4_demod_pkts(self,
                                                                callback=rx_callback,
                                                                sps=self.samples_per_symbol,
                                                                symbol_rate=self.data_rate,
                                                                threshold=-1)

        self.connect (self.packet_transmitter, (add,0))
        self.connect (noise, (add,1))
        self.connect(add,  self.packet_receiver)

    def send_pkt(self, payload='', eof=False):
        """
        Send a packet with a predetermined sequence number and from/to address.
        """
        return self.packet_transmitter.send_pkt(0xe5, struct.pack("HHHH", 0xFFFF, 0xFFFF, 0x10, 0x10), payload, eof)

    #def send_pkt(self, seqno, address, payload='', eof=False):
    #    return self.packet_transmitter.send_pkt(seqno, address, payload, eof)

def main ():

        
    def rx_callback(ok, payload):
        st.npkts += 1
        if ok:
            st.nright += 1
            (pktno,) = struct.unpack('!B', payload[2:3])
            #print "ok = %5r  pktno = %4d  len(payload) = %4d  %d/%d" % (ok, pktno, len(payload),
            #                                                            st.nright, st.npkts)
            #print "  payload: " + str(map(hex, map(ord, payload)))
	else:
	    #print "  Bad packet. %d/%d"%(st.nright, st.npkts)
	    pass

    parser = OptionParser (option_class=eng_option)
    parser.add_option("-N", "--snr", type="eng_float", default=20,
                      help="")
    parser.add_option("-n", "--nrpackets", type="int", default=100,
                      help="")

    (options, args) = parser.parse_args ()
    
    st = stats()

    fg = my_graph(rx_callback, options.snr)
    fg.start()

    for i in range(options.nrpackets):
	#print "======================="
	while fg.packet_transmitter.pkt_input.msgq().count() >= 1:
	    time.sleep(0.01)
        fg.send_pkt(payload=struct.pack('9B', 0x1, 0x80, 0x80, 0xff, 0xff, 0x10, 0x0, 0x20, 0x0))

    #fg.wait()

    print "  Statistics: good %d received %d sent %d"%(st.nright, st.npkts, options.nrpackets)
    

if __name__ == '__main__':
    # insert this in your test code...
    #import os
    #print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
    #raw_input ('Press Enter to continue: ')
    
    main ()
