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
snr_vals = np.arange(-20.0,-5.0,1.0)
enable_vals = [0.0, 0.0, 0.0]
nbytes_per_frame = 127
min_err = 10
min_ber = 0.00001
min_len = int(min_err/min_ber)
msg_interval = 10 # ms
sleeptime = 10.0

class ieee802_15_4_css_phy_self_interference(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "IEEE 802.15.4 CSS PHY Self-Interference Test")

        ##################################################
        # Variables
        ##################################################
        self.snr = snr = 0
        self.i3 = i3 = ieee802_15_4.css_phy(slow_rate=False, chirp_number=4)
        self.i2 = i2 = ieee802_15_4.css_phy(slow_rate=False, chirp_number=3)
        self.i1 = i1 = ieee802_15_4.css_phy(slow_rate=False, chirp_number=2)
        self.enable = enable = [0.0, 0.0, 0.0]
        self.c = c = ieee802_15_4.css_phy(slow_rate=False, chirp_number=1)

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_15_4_make_pair_with_blob_0_2 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(c.phy_packetsize_bytes,)))
        self.ieee802_15_4_make_pair_with_blob_0_1 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(c.phy_packetsize_bytes,)))
        self.ieee802_15_4_make_pair_with_blob_0_0 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(c.phy_packetsize_bytes,)))
        self.ieee802_15_4_make_pair_with_blob_0 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(c.phy_packetsize_bytes,)))
        self.ieee802_15_4_css_phy_tx_only_0_1 = ieee802_15_4_css_phy_tx_only(
            time_gap_2=i2.time_gap_2,
            nzeros_padding=i2.padded_zeros,
            sym_per_frame=i2.nsym_frame,
            time_gap_1=i2.time_gap_1,
            phr=i2.PHR,
            nsamp_frame=i2.nsamp_frame,
            preamble=i2.preamble,
            num_subchirps=i2.n_subchirps,
            len_sub=38,
            chirp_seq=i2.chirp_seq,
            nbytes_payload=i2.phy_packetsize_bytes,
            bits_per_cw=i2.bits_per_symbol,
            codewords=i2.codewords,
            intlv_seq=i2.intlv_seq,
            sfd=i2.SFD,
        )
        self.ieee802_15_4_css_phy_tx_only_0_0 = ieee802_15_4_css_phy_tx_only(
            time_gap_2=i3.time_gap_2,
            nzeros_padding=i3.padded_zeros,
            sym_per_frame=i3.nsym_frame,
            time_gap_1=i3.time_gap_1,
            phr=i3.PHR,
            nsamp_frame=i3.nsamp_frame,
            preamble=i3.preamble,
            num_subchirps=i3.n_subchirps,
            len_sub=38,
            chirp_seq=i3.chirp_seq,
            nbytes_payload=i3.phy_packetsize_bytes,
            bits_per_cw=i3.bits_per_symbol,
            codewords=i3.codewords,
            intlv_seq=i3.intlv_seq,
            sfd=i3.SFD,
        )
        self.ieee802_15_4_css_phy_tx_only_0 = ieee802_15_4_css_phy_tx_only(
            time_gap_2=i1.time_gap_2,
            nzeros_padding=i1.padded_zeros,
            sym_per_frame=i1.nsym_frame,
            time_gap_1=i1.time_gap_1,
            phr=i1.PHR,
            nsamp_frame=i1.nsamp_frame,
            preamble=i1.preamble,
            num_subchirps=i1.n_subchirps,
            len_sub=38,
            chirp_seq=i1.chirp_seq,
            nbytes_payload=i1.phy_packetsize_bytes,
            bits_per_cw=i1.bits_per_symbol,
            codewords=i1.codewords,
            intlv_seq=i1.intlv_seq,
            sfd=i1.SFD,
        )
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
        self.blocks_multiply_const_vxx_1_1 = blocks.multiply_const_vcc((enable[1], ))
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vcc((enable[2], ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((enable[0], ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1.1507, ))
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.5*(10**(-snr/20)), 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.ieee802_15_4_css_phy_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.ieee802_15_4_css_phy_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.ieee802_15_4_css_phy_tx_only_0_1, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.ieee802_15_4_css_phy_tx_only_0_0, 0), (self.blocks_multiply_const_vxx_1_1, 0))
        self.connect((self.ieee802_15_4_css_phy_tx_only_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1_1, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_add_xx_0, 3))

        ##################################################
        # Asynch Message Connections
        ##################################################
        # self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.msg_strobe, "strobe", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_css_phy_0, "txin")
        # self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0_2, "in")
        # self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0_0, "in")
        # self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0_1, "in")
        self.msg_connect(self.msg_strobe, "strobe", self.ieee802_15_4_make_pair_with_blob_0_2, "in")
        self.msg_connect(self.msg_strobe, "strobe", self.ieee802_15_4_make_pair_with_blob_0_0, "in")
        self.msg_connect(self.msg_strobe, "strobe", self.ieee802_15_4_make_pair_with_blob_0_1, "in")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0_2, "out", self.ieee802_15_4_css_phy_tx_only_0, "txin")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0_0, "out", self.ieee802_15_4_css_phy_tx_only_0_0, "txin")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0_1, "out", self.ieee802_15_4_css_phy_tx_only_0_1, "txin")
        self.msg_connect(self.ieee802_15_4_css_phy_0, "rxout", self.ieee802_15_4_compare_blobs_0, "test")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_compare_blobs_0, "ref")


    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.analog_noise_source_x_0.set_amplitude(0.5*(10**(-self.snr/20)))

    def get_i3(self):
        return self.i3

    def set_i3(self, i3):
        self.i3 = i3
        self.ieee802_15_4_css_phy_tx_only_0_0.set_time_gap_2(self.i3.time_gap_2)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_nzeros_padding(self.i3.padded_zeros)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_sym_per_frame(self.i3.nsym_frame)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_time_gap_1(self.i3.time_gap_1)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_phr(self.i3.PHR)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_nsamp_frame(self.i3.nsamp_frame)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_preamble(self.i3.preamble)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_num_subchirps(self.i3.n_subchirps)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_chirp_seq(self.i3.chirp_seq)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_nbytes_payload(self.i3.phy_packetsize_bytes)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_bits_per_cw(self.i3.bits_per_symbol)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_codewords(self.i3.codewords)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_intlv_seq(self.i3.intlv_seq)
        self.ieee802_15_4_css_phy_tx_only_0_0.set_sfd(self.i3.SFD)

    def get_i2(self):
        return self.i2

    def set_i2(self, i2):
        self.i2 = i2
        self.ieee802_15_4_css_phy_tx_only_0_1.set_time_gap_2(self.i2.time_gap_2)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_nzeros_padding(self.i2.padded_zeros)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_sym_per_frame(self.i2.nsym_frame)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_time_gap_1(self.i2.time_gap_1)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_phr(self.i2.PHR)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_nsamp_frame(self.i2.nsamp_frame)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_preamble(self.i2.preamble)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_num_subchirps(self.i2.n_subchirps)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_chirp_seq(self.i2.chirp_seq)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_nbytes_payload(self.i2.phy_packetsize_bytes)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_bits_per_cw(self.i2.bits_per_symbol)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_codewords(self.i2.codewords)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_intlv_seq(self.i2.intlv_seq)
        self.ieee802_15_4_css_phy_tx_only_0_1.set_sfd(self.i2.SFD)

    def get_i1(self):
        return self.i1

    def set_i1(self, i1):
        self.i1 = i1
        self.ieee802_15_4_css_phy_tx_only_0.set_time_gap_2(self.i1.time_gap_2)
        self.ieee802_15_4_css_phy_tx_only_0.set_nzeros_padding(self.i1.padded_zeros)
        self.ieee802_15_4_css_phy_tx_only_0.set_sym_per_frame(self.i1.nsym_frame)
        self.ieee802_15_4_css_phy_tx_only_0.set_time_gap_1(self.i1.time_gap_1)
        self.ieee802_15_4_css_phy_tx_only_0.set_phr(self.i1.PHR)
        self.ieee802_15_4_css_phy_tx_only_0.set_nsamp_frame(self.i1.nsamp_frame)
        self.ieee802_15_4_css_phy_tx_only_0.set_preamble(self.i1.preamble)
        self.ieee802_15_4_css_phy_tx_only_0.set_num_subchirps(self.i1.n_subchirps)
        self.ieee802_15_4_css_phy_tx_only_0.set_chirp_seq(self.i1.chirp_seq)
        self.ieee802_15_4_css_phy_tx_only_0.set_nbytes_payload(self.i1.phy_packetsize_bytes)
        self.ieee802_15_4_css_phy_tx_only_0.set_bits_per_cw(self.i1.bits_per_symbol)
        self.ieee802_15_4_css_phy_tx_only_0.set_codewords(self.i1.codewords)
        self.ieee802_15_4_css_phy_tx_only_0.set_intlv_seq(self.i1.intlv_seq)
        self.ieee802_15_4_css_phy_tx_only_0.set_sfd(self.i1.SFD)

    def get_enable(self):
        return self.enable

    def set_enable(self, enable):
        self.enable = enable
        self.blocks_multiply_const_vxx_1.set_k((self.enable[0], ))
        self.blocks_multiply_const_vxx_1_1.set_k((self.enable[1], ))
        self.blocks_multiply_const_vxx_1_0.set_k((self.enable[2], ))

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
    plt.show()
    plt.savefig("ber_self_interference_css_slow_rate-"+str(tb.c.slow_rate)+"_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"))