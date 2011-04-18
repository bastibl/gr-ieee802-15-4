#!/usr/bin/env python

#
# Decoder of IEEE 802.15.4 RADIO Packets.
#
# Modified by: Thomas Schmid
# 
# Modified for multi-channel by: Mikhail Tadjikov & Leslie Choong
#
# For more information on design:
# http://nesl.ee.ucla.edu/fw/zigbee_capture/leslie_choong_multichannel_ieee802154.pdf
#
from gnuradio import gr, eng_notation
from gnuradio import usrp2
from gnuradio import ucla
from gnuradio import blks2
from gnuradio.ucla_blks import ieee802_15_4_pkt
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import math, struct, time, sys

class stats(object):
    def __init__(self):
        self.npkts = 0
        self.nright = 0

class oqpsk_rx_graph (gr.top_block):
    def __init__(self, options, rx_callback):
        gr.top_block.__init__(self)

        u = usrp2.source_32fc(options.interface, options.mac_addr)

        self.usrp_decim = 4
        self.samples_per_symbol = 2
        self.filter_decim = 5
        self.resamp_interp = 4
        self.resamp_decim = 5

        self.data_rate = int (u.adc_rate()
                              / self.samples_per_symbol
                              / self.usrp_decim
                              / self.filter_decim
                              * self.resamp_interp
                              / self.resamp_decim)
        self.sampling_rate = int (u.adc_rate() / self.usrp_decim)

        print "data_rate = ", eng_notation.num_to_str(self.data_rate)
        print "samples_per_symbol = ", self.samples_per_symbol
        print "usrp_decim = ", self.usrp_decim
        print "usrp2_gain = ", options.gain
        print "Squelch filter = ", options.squelch

        self.chan1_freq = ieee802_15_4_pkt.chan_802_15_4.chan_map[options.channel1]
        self.chan1_num = options.channel1
        self.chan2_num = self.chan1_num + 1
        self.chan3_num = self.chan2_num + 1
        self.chan4_num = self.chan3_num + 1
        self.chan5_num = self.chan4_num + 1

        self.chan5_freq = ieee802_15_4_pkt.chan_802_15_4.chan_map[self.chan5_num]

        self.usrp_freq = (self.chan1_freq + self.chan5_freq) / 2

        self.chan1_offset = self.usrp_freq - self.chan1_freq
        self.chan2_offset = self.chan1_offset - 5000000
        self.chan3_offset = self.chan2_offset - 5000000
        self.chan4_offset = self.chan3_offset - 5000000
        self.chan5_offset = self.chan4_offset - 5000000

        print "Centering USRP2 at = ", self.usrp_freq
        print "Channel ", self.chan1_num, " freq = ", self.usrp_freq - self.chan1_offset
        print "Channel ", self.chan2_num, " freq = ", self.usrp_freq - self.chan2_offset
        print "Channel ", self.chan3_num, " freq = ", self.usrp_freq - self.chan3_offset
        print "Channel ", self.chan4_num, " freq = ", self.usrp_freq - self.chan4_offset
        print "Channel ", self.chan5_num, " freq = ", self.usrp_freq - self.chan5_offset

        u.set_center_freq(self.usrp_freq)
        u.set_decim(self.usrp_decim)
        u.set_gain(options.gain)


        # Creating a filter for channel selection
        chan_coeffs = gr.firdes.low_pass(   1.0, # filter gain
                self.sampling_rate,              # sampling rate
                2e6,                           # cutoff frequency  
                2e6,                           # bandwidth
                gr.firdes.WIN_HANN)              # filter type           

        print "Length of chan_coeffs = ", len(chan_coeffs)

        # Decimating channel filters 
        self.ddc1 = gr.freq_xlating_fir_filter_ccf(
                     self.filter_decim,  # decimation rate
                     chan_coeffs,        # taps
                     self.chan1_offset,  # frequency translation amount  
                     self.sampling_rate) # input sampling rate   

        self.ddc2 = gr.freq_xlating_fir_filter_ccf(
                     self.filter_decim,  # decimation rate
                     chan_coeffs,        # taps
                     self.chan2_offset,  # frequency translation amount  
                     self.sampling_rate) # input sampling rate   

        self.ddc3 = gr.fir_filter_ccf(self.filter_decim, chan_coeffs)

        self.ddc4 = gr.freq_xlating_fir_filter_ccf(
                     self.filter_decim,  # decimation rate
                     chan_coeffs,        # taps
                     self.chan4_offset,  # frequency translation amount  
                     self.sampling_rate) # input sampling rate   

        self.ddc5 = gr.freq_xlating_fir_filter_ccf(
                     self.filter_decim,  # decimation rate
                     chan_coeffs,        # taps
                     self.chan5_offset,  # frequency translation amount  
                     self.sampling_rate) # input sampling rate   

        self.packet_receiver1 = ieee802_15_4_pkt.ieee802_15_4_demod_pkts(
            self,
            callback=rx_callback,
            sps=self.samples_per_symbol,
            channel=self.chan1_num,
            threshold=-1)
        self.packet_receiver2 = ieee802_15_4_pkt.ieee802_15_4_demod_pkts(
            self,
            callback=rx_callback,
            sps=self.samples_per_symbol,
            channel=self.chan2_num,
            threshold=-1)
        self.packet_receiver3 = ieee802_15_4_pkt.ieee802_15_4_demod_pkts(
            self,
            callback=rx_callback,
            sps=self.samples_per_symbol,
            channel=self.chan3_num,
            threshold=-1)
        self.packet_receiver4 = ieee802_15_4_pkt.ieee802_15_4_demod_pkts(
            self,
            callback=rx_callback,
            sps=self.samples_per_symbol,
            channel=self.chan4_num,
            threshold=-1)
        self.packet_receiver5 = ieee802_15_4_pkt.ieee802_15_4_demod_pkts(
            self,
            callback=rx_callback,
            sps=self.samples_per_symbol,
            channel=self.chan5_num,
            threshold=-1)

        self.resampler1 = blks2.rational_resampler_ccf(self.resamp_interp,self.resamp_decim)
        self.resampler2 = blks2.rational_resampler_ccf(self.resamp_interp,self.resamp_decim)
        self.resampler3 = blks2.rational_resampler_ccf(self.resamp_interp,self.resamp_decim)
        self.resampler4 = blks2.rational_resampler_ccf(self.resamp_interp,self.resamp_decim)
        self.resampler5 = blks2.rational_resampler_ccf(self.resamp_interp,self.resamp_decim)

        self.u = u
        self.squelch = gr.pwr_squelch_cc(options.squelch, gate=True)

        self.connect(self.u,self.squelch)
        self.connect(self.squelch, self.ddc1,
                self.resampler1,
                self.packet_receiver1)
        self.connect(self.squelch, self.ddc2,
                self.resampler2,
                self.packet_receiver2)
        self.connect(self.squelch, self.ddc3,
                self.resampler3,
                self.packet_receiver3)
        self.connect(self.squelch, self.ddc4,
                self.resampler4,
                self.packet_receiver4)
        self.connect(self.squelch, self.ddc5,
                self.resampler5,
                self.packet_receiver5)

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

    parser = OptionParser (option_class=eng_option)
    parser.add_option ("-c", "--channel1", type="int", default=2475000000,
            help="First channel to capture on", metavar="FREQ")
    parser.add_option ("-f", "--filename", type="string",
            default="rx.dat", help="write data to FILENAME")
    parser.add_option ("-g", "--gain", type="eng_float", default=40,
            help="set Rx gain in dB [0,70]")
    parser.add_option ("-s", "--squelch", type="eng_float", default=-40.0,
            help="Set Squelch filter level")
    parser.add_option("-e", "--interface", type="string", default="eth0",
            help="select Ethernet interface, default is eth0")
    parser.add_option("-m", "--mac-addr", type="string", default="",
            help="select USRP by MAC address, default is auto-select")


    (options, args) = parser.parse_args ()

    st1 = stats()
    st2 = stats()

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

    r = gr.enable_realtime_scheduling()
    if r == gr.RT_OK:
        print "Enabled Realtime"
    else:
        print "Failed to enable Realtime. Did you run as root?"

    tb = oqpsk_rx_graph(options, rx_callback)   

    tb.start()

    tb.wait()

if __name__ == '__main__':
    # insert this in your test code...
    #import os
    #print 'Blocked waiting for GDB attach (pid = %d)' % (os.getpid(),)
    #raw_input ('Press Enter to continue: ')

    main()
