#!/usr/bin/env python

#
# Decodes CC1k and CC2420 packets simultaniously. We use
# 8-bit data streams, thus, the CC1K needs to be near the
# antenna of the USRP or we don't receive it (signal too
# weak).
#
# We assume that the FLEX2400 is on side A and FL400 on
# side B!
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
import math, struct, time, sys

class stats(object):
    def __init__(self):
        self.npkts = 0
        self.nright = 0
        
    
class rx_graph (gr.flow_graph):
    def __init__(self, rx_callback_cc2420, rx_callback_cc1k):
        gr.flow_graph.__init__(self)
        cc2420_cordic_freq = 2475000000
        cc2420_data_rate = 2000000
        cc1k_cordic_freq = 434845200
        cc1k_data_rate = 38400
        cc1k_sps = 8
        payload_size = 128
        print "cc2420_cordic_freq = %s" % (eng_notation.num_to_str (cc2420_cordic_freq))
        print "cc1k_cordic_freq = %s" % (eng_notation.num_to_str (cc1k_cordic_freq))


        # ----------------------------------------------------------------

        self.data_rate = cc2420_data_rate
        self.samples_per_symbol = 2
        self.usrp_decim = int (64e6 / self.samples_per_symbol / self.data_rate)
        self.fs = self.data_rate * self.samples_per_symbol
        payload_size = 128             # bytes

        print "usrp_decim = ", self.usrp_decim
        print "fs = ", eng_notation.num_to_str(self.fs)

        u = usrp.source_c (0, nchan=2)
        u.set_decim_rate(self.usrp_decim)
        self.subdev = (u.db[0][0], u.db[1][0])
        print "Using RX d'board %s" % (self.subdev[0].side_and_name(),)
        print "Using RX d'board %s" % (self.subdev[1].side_and_name(),)
        u.set_mux(0x2301)
        
        width = 8
        shift = 8
        format = u.make_format(width, shift)
        r = u.set_format(format)

        #this is the cc2420 code
        u.tune(self.subdev[0]._which, self.subdev[0], cc2420_cordic_freq)
        u.tune(self.subdev[1]._which, self.subdev[1], cc1k_cordic_freq)
        
        u.set_pga(0, 0)
        u.set_pga(1, 0)

        self.u = u

        # deinterleave two channels from FPGA
        di = gr.deinterleave(gr.sizeof_gr_complex)
        
        # wire up the head of the chain
        self.connect(self.u, di)
        #self.u = gr.file_source(gr.sizeof_gr_complex, 'rx_test.dat')

        # CC2420 receiver
        self.packet_receiver = ieee802_15_4_pkt.ieee802_15_4_demod_pkts(self,
                                                                        callback=rx_callback_cc2420,
                                                                        sps=self.samples_per_symbol,
                                                                        symbol_rate=self.data_rate,
                                                                        threshold=-1)

        self.squelch = gr.pwr_squelch_cc(50, 1, 0, True)
        self.connect((di,0), self.squelch, self.packet_receiver)

        # CC1K receiver
        gain_mu = 0.002*self.samples_per_symbol
        self.packet_receiver_cc1k = cc1k_sos_pkt.cc1k_demod_pkts(self,
                                                        callback=rx_callback_cc1k,
                                                        sps=cc1k_sps,
                                                        symbol_rate=cc1k_data_rate,
                                                        p_size=payload_size,
                                                        threshold=-1)
        
        #self.squelch2 = gr.pwr_squelch_cc(50, 1, 0, True)
        keep = gr.keep_one_in_n(gr.sizeof_gr_complex, 13)
        #self.connect((di, 1), keep, self.squelch2, self.packet_receiver_cc1k)
        self.connect((di, 1), keep, self.packet_receiver_cc1k)
        
def main ():

    def rx_callback_cc2420(ok, payload):
        st_cc2420.npkts += 1
        print " ------------------------"
        if ok:
            st_cc2420.nright += 1

            (pktno,) = struct.unpack('!B', payload[2:3])
            print "ok = %5r  pktno = %4d  len(payload) = %4d  cc2420 pkts: %d/%d" % (ok, pktno, len(payload),
                                                                                     st_cc2420.nright, st_cc2420.npkts)
            # for the sos head
            #(am_group, addr_mode, dst_addr, src_addr, module_dst, module_src, msg_type) = struct.unpack("HHHHBBB", payload[0:11])
            (am_group, module_dst, module_src, dst_addr, src_addr, msg_type) = struct.unpack("<BBBHHB", payload[11:19])
            msg_payload = payload[19:-2]
            (crc, ) = struct.unpack("!H", payload[-2:])
            
            print " am group: " + str(am_group)
            print "  src_addr: "+str(src_addr)+" dst_addr: "+str(dst_addr)
            print "  src_module: " + str(module_src) + " dst_module: " + str(module_dst)
            print "  msg type: " + str(msg_type)
            print "  msg: " + str(map(hex, map(ord, payload[20:-2])))
            print "  crc: " + str(hex(crc))
        else:
            print "ok = %5r pkts: %d/%d" % (ok, st_cc2420.nright, st_cc2420.npkts)
        print " ------------------------"
        sys.stdout.flush()

    def rx_callback_cc1k(ok, am_group, src_addr, dst_addr, module_src, module_dst, msg_type, msg_payload, crc):
        st_cc1k.npkts += 1
        if ok:
            st_cc1k.nright += 1

            print "ok = %5r  cc1k pkts: %d/%d" % (ok, st_cc1k.nright, st_cc1k.npkts)
            print " am group: " + str(am_group)
            print "  src_addr: "+str(src_addr)+" dst_addr: "+str(dst_addr)
            print "  src_module: " + str(module_src) + " dst_module: " + str(module_dst)
            print "  msg type: " + str(msg_type)
            print "  msg: " + str(map(hex, map(ord, msg_payload)))
            print "  crc: " + str(crc)
        else:
            print "ok = %5r pkts: %d/%d" % (ok, st_cc2420.nright, st_cc2420.npkts)

        print " ++++++++++++++++++++++++"

        
    st_cc1k = stats()
    st_cc2420 = stats()
    
    fg = rx_graph(rx_callback_cc2420, rx_callback_cc1k)
    fg.start()

    fg.wait()

if __name__ == '__main__':
    # insert this in your test code...
    #import os
    #print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
    #raw_input ('Press Enter to continue: ')
    
    main ()
