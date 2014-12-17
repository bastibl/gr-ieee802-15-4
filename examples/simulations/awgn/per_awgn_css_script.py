#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: per AWGN Test CSS SD/HD vs OQPSK
# Author: Felix Wunsch
# Generated: Mon Nov 10 19:00:50 2014
##################################################

execfile("/home/wunsch/.grc_gnuradio/ieee802_15_4_css_phy_sd.py")
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
snr_vals = np.arange(-25.0,-5.0,.5)
enable_vals = [0.0, 0.0, 0.0]
nbytes_phy_frame = 1
nbytes_mac_frame = nbytes_phy_frame + 11
min_err = 5e2
min_len = 1e3
msg_interval = 2 # ms
sleeptime = 1.0
slow_mode = True

class per_awgn_comp_nogui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "PER AWGN Test CSS SD/HD vs OQPSK")

        ##################################################
        # Variables
        ##################################################
        self.snr = snr = 0
        self.c = c = ieee802_15_4.css_phy(slow_rate=slow_mode, phy_packetsize_bytes=nbytes_mac_frame)

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_15_4_make_pair_with_blob_0 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(nbytes_phy_frame,)))
        self.ieee802_15_4_css_phy_sd_0 = ieee802_15_4_css_phy_sd(
            phr=c.PHR,
            nbytes_payload=c.phy_packetsize_bytes,
            bits_per_cw=c.bits_per_symbol,
            codewords=c.codewords,
            intlv_seq=c.intlv_seq,
            sym_per_frame=c.nsym_frame,
            num_subchirps=c.n_subchirps,
            chirp_seq=c.chirp_seq,
            time_gap_1=c.time_gap_1,
            time_gap_2=c.time_gap_2,
            len_sub=38,
            nzeros_padding=c.padded_zeros,
            preamble=c.preamble,
            sfd=c.SFD,
            nsamp_frame=c.nsamp_frame,
        )

        self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol("trigger")), msg_interval, -1, True, False)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1.1507, ))
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.5*(10**(-snr/20)), 0)
        self.mac = ieee802_15_4.mac(debug=False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.ieee802_15_4_css_phy_sd_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.ieee802_15_4_css_phy_sd_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.mac, "app in")
        self.msg_connect(self.mac, "pdu out", self.ieee802_15_4_css_phy_sd_0, "txin")
        self.msg_connect(self.ieee802_15_4_css_phy_sd_0, "rxout", self.mac, "pdu in")

    def set_snr(self, snr):
        self.snr = snr
        self.analog_noise_source_x_0_0.set_amplitude(0.5*(10**(-snr/20)))

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."

    print "Simulate from", min(snr_vals), "to", max(snr_vals), "dB SNR"
    print "Collect",min_len,"bytes per step"
    old_len_res = 0
    per_vals = []
    for i in range(len(snr_vals)):
        t0 = time.time()
        tb = None
        tb = per_awgn_comp_nogui()
        tb.set_snr(snr_vals[i])
        tb.start()
        time.sleep(1)
        per = 1.0
        while(True):
            len_res = tb.mac.get_num_packets_received()
            print snr_vals[i], "dB:", 100.0*len_res/min_len, "% done"
            if(len_res >= min_len):
                if tb.mac.get_num_packet_errors() > min_err or tb.mac.get_num_packets_received() > 10*min_len:
                    tb.stop()
                    tb.wait()
                    time.sleep(1)
                    break
            # if(per_hd == 0 and per_sd == 0 ):
            #     tb.stop()
            #     tb.wait()
            #     time.sleep(1)
            #     break
            time.sleep(sleeptime)
            old_len_res = len_res

        per = tb.mac.get_packet_error_ratio()
        print "PER at", snr_vals[i], "dB SNR (SD):", per, "(", tb.mac.get_num_packet_errors(), "/", tb.mac.get_num_packets_received(), ")"
        per_vals.append(per)
        t_elapsed = time.time() - t0
        print "approximately",t_elapsed*(len(snr_vals)-i-1)/60, "minutes remaining"
        np.save("tmp_per_awgn_css_slow_rate-"+str(tb.c.slow_rate)+"_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB", per_vals)

    np.save("per_awgn_css_slow_rate-"+str(tb.c.slow_rate)+"_packetlen-"+str(nbytes_mac_frame)+"bytes_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"), per_vals)
    plt.plot(snr_vals, per_vals)
    plt.yscale('log')
    plt.grid()
    plt.xlabel("SNR")
    plt.ylabel("PER")
    plt.title("per_awgn_css_slow-rate-"+str(tb.c.slow_rate)+"_packetlen-"+str(nbytes_mac_frame)+"bytes_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"))
    plt.savefig("per_awgn_css_slow-rate-"+str(tb.c.slow_rate)+"_packetlen-"+str(nbytes_mac_frame)+"bytes_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")
    plt.show()
