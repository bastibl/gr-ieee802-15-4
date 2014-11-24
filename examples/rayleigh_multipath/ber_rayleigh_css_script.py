#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: BER AWGN Test CSS SD/HD vs OQPSK
# Author: Felix Wunsch
# Generated: Mon Nov 10 19:00:50 2014
##################################################

execfile("/home/felixwunsch/.grc_gnuradio/ieee802_15_4_css_phy_hd.py")
execfile("/home/felixwunsch/.grc_gnuradio/ieee802_15_4_css_phy_sd.py")
execfile("/home/felixwunsch/.grc_gnuradio/ieee802_15_4_oqpsk_phy_nosync.py")
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
noise_ampl_vals = np.arange(-10.0,10.0,1.0)
nbytes_per_frame = 127
cfg = ieee802_15_4.css_phy(slow_rate=True, phy_packetsize_bytes=nbytes_per_frame)
min_err = 10
min_ber = 0.0001
min_len = int(min_err/min_ber)
nframes = float(min_len)/nbytes_per_frame
nsamps_total = nframes*FIXME
pdp = [np.exp(-21586735.0*tau) for tau in np.arange(0.0,320*1e-9, 1.0/(32*1e6))]
coherence_time_samps = FIXME

class ber_rayleigh_comp_nogui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "BER AWGN Test CSS SD/HD vs OQPSK")

        ##################################################
        # Variables
        ##################################################
        self.snr = snr = 0
        self.c = c = cfg

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_15_4_oqpsk_phy_nosync_0 = ieee802_15_4_oqpsk_phy_nosync(
            payload_len=c.phy_packetsize_bytes,
        )
        self.ieee802_15_4_make_pair_with_blob_0 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(c.phy_packetsize_bytes,)))
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
        self.ieee802_15_4_css_phy_hd_0 = ieee802_15_4_css_phy_hd(
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
        self.ieee802_15_4_rayleigh_channel_sim_hd = ieee802_15_4.rayleigh_multipath_cc(pdp, coherence_time_samps) 
        self.ieee802_15_4_rayleigh_channel_sim_sd = ieee802_15_4.rayleigh_multipath_cc(pdp, coherence_time_samps)
        self.skip_fir_group_delay = blocks.skiphead(gr.sizeof_gr_complex, (len(pdp)-1)/2)
        self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol("trigger")), 10, -1, True, False)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((1.1687, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1.1687, ))
        self.blocks_add_xx_0_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 10**(-snr/10), 0)
        self.comp_bits_sd = ieee802_15_4.compare_blobs()
        self.comp_bits_hd = ieee802_15_4.compare_blobs()

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.ieee802_15_4_css_phy_sd_0, 0))
        self.connect((self.ieee802_15_4_css_phy_sd_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.ieee802_15_4_css_phy_hd_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0_1, 1))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0_1, 0))
        self.connect((self.blocks_add_xx_0_1, 0), (self.ieee802_15_4_css_phy_hd_0, 0))

        self.connect(self.analog_noise_source_x_0_0, self.noise_snk)
        self.connect(self.blocks_multiply_const_vxx_0, self.sig_snk)

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_css_phy_sd_0, "txin")
        self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_css_phy_hd_0, "txin")
        self.msg_connect(self.ieee802_15_4_css_phy_sd_0, "rxout", self.comp_bits_sd, "test")
        self.msg_connect(self.ieee802_15_4_css_phy_hd_0, "rxout", self.comp_bits_hd, "test")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.comp_bits_hd, "ref")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.comp_bits_sd, "ref")
        # self.msg_connect(self.ieee802_15_4_css_phy_sd_0, "rxout", self.ieee802_15_4_make_pair_with_blob_0, "in")

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.analog_noise_source_x_0_0.set_amplitude(10**(-self.snr/10))

    def get_c(self):
        return self.c

    def set_c(self, c):
        self.c = c
        self.ieee802_15_4_css_phy_sd_0.set_phr(self.c.PHR)
        self.ieee802_15_4_css_phy_sd_0.set_nbytes_payload(self.c.phy_packetsize_bytes)
        self.ieee802_15_4_css_phy_sd_0.set_bits_per_cw(self.c.bits_per_symbol)
        self.ieee802_15_4_css_phy_sd_0.set_codewords(self.c.codewords)
        self.ieee802_15_4_css_phy_sd_0.set_intlv_seq(self.c.intlv_seq)
        self.ieee802_15_4_css_phy_sd_0.set_sym_per_frame(self.c.nsym_frame)
        self.ieee802_15_4_css_phy_sd_0.set_num_subchirps(self.c.n_subchirps)
        self.ieee802_15_4_css_phy_sd_0.set_chirp_seq(self.c.chirp_seq)
        self.ieee802_15_4_css_phy_sd_0.set_time_gap_1(self.c.time_gap_1)
        self.ieee802_15_4_css_phy_sd_0.set_time_gap_2(self.c.time_gap_2)
        self.ieee802_15_4_css_phy_sd_0.set_nzeros_padding(self.c.padded_zeros)
        self.ieee802_15_4_css_phy_sd_0.set_preamble(self.c.preamble)
        self.ieee802_15_4_css_phy_sd_0.set_sfd(self.c.SFD)
        self.ieee802_15_4_css_phy_sd_0.set_nsamp_frame(self.c.nsamp_frame)
        self.ieee802_15_4_css_phy_hd_0.set_phr(self.c.PHR)
        self.ieee802_15_4_css_phy_hd_0.set_nbytes_payload(self.c.phy_packetsize_bytes)
        self.ieee802_15_4_css_phy_hd_0.set_bits_per_cw(self.c.bits_per_symbol)
        self.ieee802_15_4_css_phy_hd_0.set_codewords(self.c.codewords)
        self.ieee802_15_4_css_phy_hd_0.set_intlv_seq(self.c.intlv_seq)
        self.ieee802_15_4_css_phy_hd_0.set_sym_per_frame(self.c.nsym_frame)
        self.ieee802_15_4_css_phy_hd_0.set_num_subchirps(self.c.n_subchirps)
        self.ieee802_15_4_css_phy_hd_0.set_chirp_seq(self.c.chirp_seq)
        self.ieee802_15_4_css_phy_hd_0.set_time_gap_1(self.c.time_gap_1)
        self.ieee802_15_4_css_phy_hd_0.set_time_gap_2(self.c.time_gap_2)
        self.ieee802_15_4_css_phy_hd_0.set_nzeros_padding(self.c.padded_zeros)
        self.ieee802_15_4_css_phy_hd_0.set_preamble(self.c.preamble)
        self.ieee802_15_4_css_phy_hd_0.set_sfd(self.c.SFD)
        self.ieee802_15_4_css_phy_hd_0.set_nsamp_frame(self.c.nsamp_frame)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."

    snr_vals = np.arange(-10.0,8.0,0.5)
    min_err = 100
    min_ber = 0.00001
    min_len = int(min_err/min_ber)
    if min_len <= 1e3:
        raise Exception("min_len too short")
    print "Simulate from", min(snr_vals), "to", max(snr_vals), "dB SNR"
    print "Collect",min_len,"bytes per step"
    old_len_res = 0
    ber_vals = []
    for i in range(len(snr_vals)):
        t0 = time.time()
        tb = None
        tb = ber_rayleigh_comp_nogui()
        tb.set_snr(snr_vals[i])
        tb.start()
        time.sleep(1)
        ber_hd = 1.0
        ber_sd = 1.0
        while(True):
            len_res = [tb.comp_bits_hd.get_bits_compared(), tb.comp_bits_sd.get_bits_compared()]
            if len_res == old_len_res:
                print "simulation got stuck, restart at current position"
                tb.stop()
                tb.wait()
                t0 = time.time()
                tb = None
                tb = ber_rayleigh_comp_nogui()
                tb.set_snr(snr_vals[i])
                tb.start()      
                time.sleep(1)
                len_res = [tb.comp_bits_hd.get_bits_compared(), tb.comp_bits_sd.get_bits_compared()]         
            print snr_vals[i], "dB:", 100.0*min(len_res)/min_len, "% done"
            if(min(len_res) >= min_len):
                tb.stop()
                tb.wait()
                time.sleep(1)
                break
            if(ber_hd == 0 and ber_sd == 0 ):
                tb.stop()
                tb.wait()
                time.sleep(1)
                break
            time.sleep(10)
            old_len_res = len_res

        ber_hd = tb.comp_bits_hd.get_ber()
        ber_sd = tb.comp_bits_sd.get_ber()
        print "BER at", snr_vals[i], "dB SNR (HD/SD):", ber_hd, "/", ber_sd
        ber_vals.append((ber_hd, ber_sd))
        t_elapsed = time.time() - t0
        print "approximately",t_elapsed*(len(snr_vals)-i-1)/60, "minutes remaining"
        np.save("tmp_ber_rayleigh_css_slow_rate-"+str(tb.c.slow_rate)+"_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB", ber_vals)

    np.save("ber_rayleigh_css_slow_rate-"+str(tb.c.slow_rate)+"_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"), ber_vals)
    plt.plot(snr_vals, ber_vals)
    plt.yscale('log')
    plt.title("ber_rayleigh_css_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"))
    plt.show()
