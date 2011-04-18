#!/usr/bin/env python

#
# Decoder of IEEE 802.15.4 RADIO Packets.
#
# Modified by: Thomas Schmid, Leslie Choong, Mikhail Tadjikov
#
  
from gnuradio import gr, eng_notation, usrp2
from gnuradio.ucla_blks import ieee802_15_4_pkt
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import struct, sys, time, math

class stats(object):
    def __init__(self):
        self.npkts = 0
        self.nright = 0
        
    
class oqpsk_rx_graph (gr.top_block):
    def __init__(self, options, rx_callback):
        gr.top_block.__init__(self)

        if options.infile is None:
            # Initialize USRP2 block
            u = usrp2.source_32fc(options.interface, options.mac_addr)
            self.samples_per_symbol = 2
            self.chan_num = options.channel
            self.data_rate = int (u.adc_rate()
                                  / self.samples_per_symbol
                                  / options.decim_rate)

            u.set_center_freq(ieee802_15_4_pkt.chan_802_15_4.chan_map[self.chan_num])
            u.set_decim(options.decim_rate)
            u.set_gain(options.gain)

            print "cordic_freq = %s" % (eng_notation.num_to_str(ieee802_15_4_pkt.chan_802_15_4.chan_map[self.chan_num]))
            print "data_rate = ", eng_notation.num_to_str(self.data_rate)
            print "samples_per_symbol = ", self.samples_per_symbol
            print "usrp_decim = ", options.decim_rate

            self.src = u
        else:
            self.src = gr.file_source(gr.sizeof_gr_complex, options.infile);
            self.samples_per_symbol = 2
            self.data_rate = 2000000

        self.packet_receiver = ieee802_15_4_pkt.ieee802_15_4_demod_pkts(self,
                                callback=rx_callback,
                                sps=self.samples_per_symbol,
                                symbol_rate=self.data_rate,
                                channel=self.chan_num,
                                threshold=options.threshold)

        #self.squelch = gr.pwr_squelch_cc(-65, gate=True)
        self.connect(self.src,
         #       self.squelch,
                self.packet_receiver)

def main ():
    def rx_callback(ok, payload, chan_num):
        # Output this packet in pcap format
        pcap_capture_time = time.time()
        pcap_capture_msec = math.modf(pcap_capture_time)[0] * 1e6
        pcap_pkt_header = struct.pack('IIIIB',
                                      pcap_capture_time,
                                      pcap_capture_msec,
                                      len(payload)+1,
                                      len(payload)+1,
                                      chan_num)
        fout.write(pcap_pkt_header)
        fout.write(payload)
        fout.flush()
    def rx_callback_old(ok, payload, chan_num):
        st.npkts += 1
        if ok:
            st.nright += 1

        (pktno,) = struct.unpack('!H', payload[0:2])
        print "ok = %5r  pktno = %4d  len(payload) = %4d  %d/%d" % (ok, pktno, len(payload),
                                                                    st.nright, st.npkts)
        print "  payload: " + str(map(hex, map(ord, payload)))
        print " ------------------------"
        sys.stdout.flush()

        
    parser = OptionParser (option_class=eng_option)
    parser.add_option("-R", "--rx-subdev-spec", type="subdev", default=None,
                      help="select USRP Rx side A or B (default=first one with a daughterboard)")
    parser.add_option ("-c", "--channel", type="eng_float", default=15,
                       help="Set 802.15.4 Channel to listen on", metavar="FREQ")
    parser.add_option ("-d", "--decim_rate", type="int", default=25,
                       help="set decimation rate")
    parser.add_option ("-r", "--data-rate", type="eng_float", default=2000000)
    parser.add_option ("-f", "--filename", type="string",
                       default="rx.dat", help="write data to FILENAME")
    parser.add_option ("-i", "--infile", type="string",
                       default=None, help="Process from captured file")
    parser.add_option ("-g", "--gain", type="eng_float", default=35,
                       help="set Rx gain in dB [0,70]")
    parser.add_option ("-N", "--no-gui", action="store_true", default=False)
    parser.add_option ("-t", "--threshold", type="int", default=-1)
    parser.add_option("-e", "--interface", type="string", default="eth0",
            help="select Ethernet interface, default is eth0")
    parser.add_option("-m", "--mac-addr", type="string", default="",
            help="select USRP by MAC address, default is auto-select")

    (options, args) = parser.parse_args ()

    st = stats()

    # Setup the libpcap output file
    fout = open(options.filename, "w")
    # Write the libpcap Global Header
    pcap_glob_head = struct.pack('IHHiIII',
            0xa1b2c3d4,    # Magic Number
            2,             # Major Version Number
            4,             # Minor Version Number
            0,
            0,
            65535,
            221)           # Link Layer Type = 802.15.4 PHY Channel
    fout.write(pcap_glob_head)

    r= gr.enable_realtime_scheduling()
    if r == gr.RT_OK:
        print "Enabled Realtime"
    else:
        print "Failed to enable Realtime"

    tb = oqpsk_rx_graph(options, rx_callback)
    tb.start()

    tb.wait()

if __name__ == '__main__':
    main ()
