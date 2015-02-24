#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: BER AWGN Test CSS SD/HD vs OQPSK
# Author: Felix Wunsch
# Generated: Mon Nov 10 19:00:50 2014
##################################################

execfile("/home/wunsch/.grc_gnuradio/ieee802_15_4_css_phy_hd.py")
execfile("/home/wunsch/.grc_gnuradio/ieee802_15_4_css_phy_sd.py")
execfile("/home/wunsch/.grc_gnuradio/ieee802_15_4_oqpsk_phy_nosync.py")
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import foo
import ieee802_15_4
import numpy as np
import pmt
import time
import matplotlib.pyplot as plt

# configuration parameters
snr_vals = np.arange(-20.0,-5.0,.5)
enable_vals = [0.0, 0.0, 0.0]
nbytes_phy_frame = 1
nbytes_mac_frame = nbytes_phy_frame + 11
min_err = 1e2
min_len = 1e3
msg_interval = 2 # ms
sleeptime = 1.0

class ber_awgn_comp_nogui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "BER AWGN Test OQPSK")

        ##################################################
        # Variables
        ##################################################
        self.snr = snr = 0
        self.c = c = ieee802_15_4.css_phy(slow_rate=True, phy_packetsize_bytes=nbytes_mac_frame)

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_15_4_oqpsk_phy_nosync_0 = ieee802_15_4_oqpsk_phy_nosync(
            payload_len=c.phy_packetsize_bytes,
        )
        self.mac = ieee802_15_4.mac(debug=False)
        self.ieee802_15_4_make_pair_with_blob_0 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(nbytes_phy_frame,)))
        self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol("trigger")), msg_interval, -1, True, False)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_GAUSSIAN, np.sqrt(0.5)*(10**(-snr/20)), 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_add_xx_0_0, 0), (self.ieee802_15_4_oqpsk_phy_nosync_0, 0))
        self.connect((self.ieee802_15_4_oqpsk_phy_nosync_0, 0), (self.blocks_add_xx_0_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.mac, "app in")
        self.msg_connect(self.mac, "pdu out", self.ieee802_15_4_oqpsk_phy_nosync_0, "txin")
        self.msg_connect(self.ieee802_15_4_oqpsk_phy_nosync_0, "rxout", self.mac, "pdu in")

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.analog_noise_source_x_0_0.set_amplitude(np.sqrt(0.5)*(10**(-snr/20)))

    def get_c(self):
        return self.c

    def set_c(self, c):
        self.c = c
        self.ieee802_15_4_oqpsk_phy_nosync_0.set_payload_len(nbytes_mac_frame)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."

    min_ram_usage_mb = 2.0*min_len/1024/1024
    print "Simulation needs at least", min_ram_usage_mb, "MB of RAM"
    if min_ram_usage_mb > 4000:
        print "Careful, simulation needs more than 4GB RAM!"
    print "Simulate from", min(snr_vals), "to", max(snr_vals), "dB SNR"
    print "Collect",min_len,"bytes per step"
    per_vals = [];
    for i in range(len(snr_vals)):
        t0 = time.time()
        tb = None
        tb = ber_awgn_comp_nogui()
        tb.set_snr(snr_vals[i])
        tb.start()
        while(True):
            len_res = tb.mac.get_num_packets_received()
            print snr_vals[i], "dB:", 100.0*len_res/min_len, "% done"
            time.sleep(sleeptime)
            if(len_res >= min_len ):
                if tb.mac.get_num_packet_errors() >= min_err or len_res > min_len*20:
                    tb.stop()
                    tb.wait()
                    break

        per = tb.mac.get_packet_error_ratio()
        print "PER at", snr_vals[i], "dB SNR: ", per, "(", tb.mac.get_num_packet_errors(), "/", tb.mac.get_num_packets_received(), ")"
        per_vals.append(per)
        t_elapsed = time.time() - t0
        print "approximately",t_elapsed*(len(snr_vals)-len(per_vals))/60, "minutes remaining"

    np.save("per_awgn_oqpsk_packetlen-"+str(nbytes_mac_frame)+"bytes_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"), per_vals)
    plt.plot(snr_vals, per_vals)
    plt.yscale('log')
    plt.grid()
    plt.xlabel("SNR")
    plt.ylabel("PER")
    plt.title("per_awgn_oqpsk_packetlen-"+str(nbytes_mac_frame)+"bytes_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"))
    plt.savefig("per_awgn_oqpsk_packetlen-"+str(nbytes_mac_frame)+"bytes_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")
    plt.show()
