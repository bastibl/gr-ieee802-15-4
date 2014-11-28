#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: IEEE 802.15.4 CSS PHY Self-Interference Test
# Author: Felix Wunsch
# Description: IEEE 802.15.4 CSS PHY Self-Interference Test
# Generated: Tue Nov 25 16:59:12 2014
##################################################

execfile("/home/wunsch/.grc_gnuradio/ieee802_15_4_css_phy_sd.py")
execfile("/home/wunsch/.grc_gnuradio/ieee802_15_4_css_phy_tx_only.py")
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
snr_vals = np.arange(-25.0,-5.0,1.0)
enable_vals = [0.0, 0.0, 0.0]
nbytes_per_frame = 127
min_err = 1e3
min_len = 1e5
msg_interval = 10 # ms
sleeptime = 1.0

class ieee802_15_4_css_phy_self_interference(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "IEEE 802.15.4 CSS PHY Self-Interference Test")

        ##################################################
        # Variables
        ##################################################
        self.snr = snr = 0
        self.enable = enable = [0.0, 0.0, 0.0]
        self.c = c = ieee802_15_4.css_phy(slow_rate=False, chirp_number=1)

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_15_4_make_pair_with_blob_0 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(c.phy_packetsize_bytes,)))
        self.ieee802_15_4_css_phy_0 = ieee802_15_4_css_phy_sd(
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
        self.ieee802_15_4_compare_blobs_0 = ieee802_15_4.compare_blobs(False)
        # self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol("trigger")), msg_interval, -1, True, False)
        self.msg_strobe = blocks.message_strobe(pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol("trigger")), msg_interval)
        self.src_i1 = blocks.file_source(gr.sizeof_gr_complex, "frame_127bytes_seq2.bin", repeat=True)
        self.src_i2 = blocks.file_source(gr.sizeof_gr_complex, "frame_127bytes_seq3.bin", repeat=True)
        self.src_i3 = blocks.file_source(gr.sizeof_gr_complex, "frame_127bytes_seq4.bin", repeat=True)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((enable[1], ))
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vcc((enable[2], ))
        self.blocks_multiply_const_vxx_3 = blocks.multiply_const_vcc((enable[0], ))
        self.blocks_multiply_const_vxx_norm = blocks.multiply_const_vcc((1.1507, ))
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.5*(10**(-snr/20)), 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.ieee802_15_4_css_phy_0, 0), (self.blocks_add_xx_0, 0))
        self.connect(self.src_i1, (self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect(self.src_i2, (self.blocks_multiply_const_vxx_2, 0), (self.blocks_add_xx_0, 2))
        self.connect(self.src_i3, (self.blocks_multiply_const_vxx_3, 0), (self.blocks_add_xx_0, 3))
        self.connect(self.blocks_add_xx_0, self.blocks_multiply_const_vxx_norm)
        self.connect((self.blocks_multiply_const_vxx_norm, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.ieee802_15_4_css_phy_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.msg_strobe, "strobe", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_css_phy_0, "txin")
        self.msg_connect(self.ieee802_15_4_css_phy_0, "rxout", self.ieee802_15_4_compare_blobs_0, "test")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_compare_blobs_0, "ref")


    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.analog_noise_source_x_0.set_amplitude(0.5*(10**(-self.snr/20)))

    def get_enable(self):
        return self.enable

    def set_enable(self, enable):
        self.enable = enable
        self.blocks_multiply_const_vxx_1.set_k((self.enable[0], ))
        self.blocks_multiply_const_vxx_2.set_k((self.enable[1], ))
        self.blocks_multiply_const_vxx_3.set_k((self.enable[2], ))

    def get_c(self):
        return self.c

    def set_c(self, c):
        self.c = c
        self.ieee802_15_4_css_phy_0.set_phr(self.c.PHR)
        self.ieee802_15_4_css_phy_0.set_nbytes_payload(self.c.phy_packetsize_bytes)
        self.ieee802_15_4_css_phy_0.set_bits_per_cw(self.c.bits_per_symbol)
        self.ieee802_15_4_css_phy_0.set_codewords(self.c.codewords)
        self.ieee802_15_4_css_phy_0.set_intlv_seq(self.c.intlv_seq)
        self.ieee802_15_4_css_phy_0.set_sym_per_frame(self.c.nsym_frame)
        self.ieee802_15_4_css_phy_0.set_num_subchirps(self.c.n_subchirps)
        self.ieee802_15_4_css_phy_0.set_chirp_seq(self.c.chirp_seq)
        self.ieee802_15_4_css_phy_0.set_time_gap_1(self.c.time_gap_1)
        self.ieee802_15_4_css_phy_0.set_time_gap_2(self.c.time_gap_2)
        self.ieee802_15_4_css_phy_0.set_nzeros_padding(self.c.padded_zeros)
        self.ieee802_15_4_css_phy_0.set_preamble(self.c.preamble)
        self.ieee802_15_4_css_phy_0.set_sfd(self.c.SFD)
        self.ieee802_15_4_css_phy_0.set_nsamp_frame(self.c.nsamp_frame)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
 
    ber_vals = np.ones((4,len(snr_vals)))   
    for k in range(len(enable_vals)+1):
        if(k-1 > 0):
            enable_vals[k-1] = 1.0
        ber = 1.0
        for i in range(len(snr_vals)):
            t0 = time.time()
            tb = None
            tb = ieee802_15_4_css_phy_self_interference()
            tb.set_snr(snr_vals[i])
            tb.set_enable(enable_vals)
            time.sleep(.5) # some setup time won't hurt
            tb.start()
            while(True):
                len_res = tb.ieee802_15_4_compare_blobs_0.get_bits_compared()
                if len_res >= min_len:
                    if tb.ieee802_15_4_compare_blobs_0.get_errors_found() > min_err or len_res >= 50*min_len:
                        tb.stop()
                        tb.wait()
                        break
                print snr_vals[i], "dB:", 100.0*len_res/min_len, "% done"
                time.sleep(sleeptime)
            ber = tb.ieee802_15_4_compare_blobs_0.get_ber()
            ber_vals[k,i] = ber
            print "BER at", snr_vals[i], "dB SNR (SD) with", k, "interferers:", ber_vals[k,i]
            t_elapsed = time.time() - t0
            print "approximately",t_elapsed*len(snr_vals)*(len(enable_vals)+1-k)/60-t_elapsed*(len(snr_vals)-i-1)/60, "minutes remaining"
            np.save("tmp_ber_self_interference_css_slow_rate-"+str(tb.c.slow_rate)+"_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB", ber_vals)

    np.save("ber_self_interference_css_slow_rate-"+str(tb.c.slow_rate)+"_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"), ber_vals)
    for i in range(len(enable_vals)+1):
        plt.plot(snr_vals, ber_vals[i,:], label="# interferers: "+str(i))
    plt.legend(loc='lower left')
    plt.yscale('log')
    plt.grid()
    plt.ylabel("BER")
    plt.xlabel("SNR")
    plt.title("Influence of self interference on CSS transmissions in an AWGN channel")
    plt.savefig("ber_self_interference_css_slow_rate-"+str(tb.c.slow_rate)+"_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")
    plt.show()
