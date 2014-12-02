#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: BER AWGN Test CSS SD/HD vs OQPSK
# Author: Felix Wunsch
# Generated: Mon Nov 10 19:00:50 2014
##################################################

execfile("/home/felixwunsch/.grc_gnuradio/ieee802_15_4_oqpsk_phy_nosync.py")
execfile("/home/felixwunsch/.grc_gnuradio/ieee802_15_4_css_phy_sd.py")

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

import gc

# configuration parameters
snr_vals = -20
nbytes_per_frame = 127
cfg_slow = ieee802_15_4.css_phy(slow_rate=True, phy_packetsize_bytes=nbytes_per_frame)
cfg_fast = ieee802_15_4.css_phy(slow_rate=False, phy_packetsize_bytes=nbytes_per_frame)
min_err = 1000  # int(5e3)
min_len = 10000  # int(1e6)
msg_interval = 1  # ms
sleeptime = .1  # s
fs_oqpsk = 4e6
fs_css = 32e6
interferer_freq_oqpsk = np.arange(-fs_oqpsk/2, fs_oqpsk/2, 2e4)
interferer_freq_css = np.arange(-fs_css/2, fs_css/2, 2e5)
norm_fac = 1.1507

en_oqpsk = True
en_css_fast = True
en_css_slow = True


class ber_singletone_oqpsk(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "BER OQPSK with singletone interferer")

        ##################################################
        # Variables
        ##################################################
        self.snr = snr = 0

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_15_4_oqpsk_phy_nosync_0 = ieee802_15_4_oqpsk_phy_nosync(
            payload_len=127,
        )
        self.ieee802_15_4_make_pair_with_blob_0 = ieee802_15_4.make_pair_with_blob(
            np.random.randint(0, 256, (127,)))
        self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol("trigger")),
                                                                 msg_interval, -1, True, False)
        self.blocks_add_xx_sd = blocks.add_vcc(1)
        self.singletone_src = analog.sig_source_c(fs_oqpsk, analog.GR_COS_WAVE, interferer_freq_oqpsk[0], 10 ** (-snr / 20))
        self.comp_bits = ieee802_15_4.compare_blobs()
        # self.sig_snk = blocks.file_sink(gr.sizeof_gr_complex, "css_sig.bin")

        ##################################################
        # Connections
        ##################################################
        self.connect((self.ieee802_15_4_oqpsk_phy_nosync_0, 0), (self.blocks_add_xx_sd, 0))
        self.connect((self.singletone_src, 0), (self.blocks_add_xx_sd, 1))
        self.connect((self.blocks_add_xx_sd, 0), (self.ieee802_15_4_oqpsk_phy_nosync_0, 0))

        # self.connect(self.ieee802_15_4_css_phy_sd_0, self.sig_snk)

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_oqpsk_phy_nosync_0, "txin")
        self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.ieee802_15_4_oqpsk_phy_nosync_0, "rxout", self.comp_bits, "test")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.comp_bits, "ref")
        # self.msg_connect(self.ieee802_15_4_css_phy_sd_0, "rxout", self.ieee802_15_4_make_pair_with_blob_0, "in")

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.singletone_src.set_amplitude(10 ** (-snr / 20))

class ber_singletone_css(gr.top_block):
    def __init__(self, cfg):
        gr.top_block.__init__(self, "BER CSS with singletone interferer")

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
        self.ieee802_15_4_make_pair_with_blob_0 = ieee802_15_4.make_pair_with_blob(
            np.random.randint(0, 256, (c.phy_packetsize_bytes,)))
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
        self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol("trigger")),
                                                                 msg_interval, -1, True, False)
        self.blocks_multiply_const_vxx_sd = blocks.multiply_const_vcc((norm_fac, ))
        self.blocks_add_xx_sd = blocks.add_vcc(1)
        self.singletone_src = analog.sig_source_c(fs_css, analog.GR_COS_WAVE, interferer_freq_css[0], 10**(-snr/20))
        self.comp_bits = ieee802_15_4.compare_blobs()
        # self.sig_snk = blocks.file_sink(gr.sizeof_gr_complex, "css_sig.bin")

        ##################################################
        # Connections
        ##################################################
        self.connect((self.ieee802_15_4_css_phy_sd_0, 0), (self.blocks_multiply_const_vxx_sd, 0))
        self.connect(self.blocks_multiply_const_vxx_sd, (self.blocks_add_xx_sd, 0))
        self.connect((self.singletone_src, 0), (self.blocks_add_xx_sd, 1))
        self.connect((self.blocks_add_xx_sd, 0), (self.ieee802_15_4_css_phy_sd_0, 0))

        # self.connect(self.ieee802_15_4_css_phy_sd_0, self.sig_snk)

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_css_phy_sd_0, "txin")
        self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.ieee802_15_4_css_phy_sd_0, "rxout", self.comp_bits, "test")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.comp_bits, "ref")
        # self.msg_connect(self.ieee802_15_4_css_phy_sd_0, "rxout", self.ieee802_15_4_make_pair_with_blob_0, "in")

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.singletone_src.set_amplitude(10 ** (-snr / 20))

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

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."


    if en_oqpsk:
        # OQPSK
        if min_len <= 1e3:
            print "WARNING: min_len very short:", min_len
        print "Collect", min_len, "bytes per step"
        old_len_res = 0
        ber_vals = []
        for i in range(len(interferer_freq_oqpsk)):
            tb=None
            gc.collect()
            t0 = time.time()
            tb = ber_singletone_oqpsk()
            tb.set_snr(snr_vals)
            tb.singletone_src.set_frequency(interferer_freq_oqpsk[i])
            tb.start()
            time.sleep(.1)
            ber = 1.0
            while (True):
                len_res = tb.comp_bits.get_bits_compared()
                # print interferer_freq_oqpsk[i]/1000000, "MHz:", 100.0 * len_res / min_len, "% done"
                if (len_res >= min_len):
                    if (tb.comp_bits.get_errors_found() >= min_err or tb.comp_bits.get_bits_compared() >= 10 * min_len):
                        print "Found a total of", tb.comp_bits.get_errors_found(), " errors"
                        tb.stop()
                        break
                    else:
                        print "Found", tb.comp_bits.get_errors_found(), "of", min_err, "errors"
                if (ber == 0 ):
                    tb.stop()
                    tb.wait()
                    time.sleep(.1)
                    break
                time.sleep(sleeptime)
                old_len_res = len_res

            ber = tb.comp_bits.get_ber()
            print "Step", i + 1, "/", len(interferer_freq_oqpsk), ": BER at", interferer_freq_oqpsk[i]/1e6, "MHz:", ber
            ber_vals.append(ber)
            t_elapsed = time.time() - t0
            print "approximately", t_elapsed * (len(interferer_freq_oqpsk) - i - 1) / 60, "minutes remaining"
            np.save("tmp_ber_singletone_oqpsk_" + str(min(interferer_freq_oqpsk/1e6)) + "_to_" + str(
                max(interferer_freq_oqpsk/1e6)) + "MHz", ber_vals)

        name = "ber_singletone_oqpsk_" + str(min(interferer_freq_oqpsk/1e6)) + "_to_" + str(
            max(interferer_freq_oqpsk/1e6)) + "MHz_" + time.strftime("%Y-%m-%d_%H-%M-%S")
        np.save(name, ber_vals)
        try:
            plt.plot(interferer_freq_oqpsk, ber_vals, label="SIR=" + str(snr_vals) + " dB")
            plt.legend(loc='lower left')
            plt.xlabel("Frequency [Hz]")
            plt.xlim([-fs_oqpsk/2, fs_oqpsk/2])
            plt.ylabel("BER")
            plt.grid()
            plt.yscale('log')
            plt.title(name)
            plt.savefig(name + ".pdf")
            plt.clear()
        except:
            print "plotting OQPSK curve failed"
            pass

    if en_css_fast:
        # CSS fast
        if min_len <= 1e3:
            print "WARNING: min_len very short:", min_len
        print "Collect", min_len, "bytes per step"
        old_len_res = 0
        ber_vals = []
        for i in range(len(interferer_freq_css)):
            t0 = time.time()
            tb = None
            gc.collect()
            tb = ber_singletone_css(cfg_fast)
            tb.set_snr(snr_vals)
            tb.singletone_src.set_frequency(interferer_freq_css[i])
            tb.start()
            time.sleep(.1)
            ber = 1.0
            while (True):
                len_res = tb.comp_bits.get_bits_compared()
                print interferer_freq_css[i]/1000000, "MHz:", 100.0 * len_res / min_len, "% done"
                if (len_res >= min_len):
                    if (tb.comp_bits.get_errors_found() >= min_err or tb.comp_bits.get_bits_compared() >= 10 * min_len):
                        print "Found a total of", tb.comp_bits.get_errors_found(), " errors"
                        tb.stop()
                        break
                    else:
                        print "Found", tb.comp_bits.get_errors_found(), "of", min_err, "errors"
                if (ber == 0 ):
                    tb.stop()
                    tb.wait()
                    time.sleep(.1)
                    break
                time.sleep(sleeptime)
                old_len_res = len_res

            ber = tb.comp_bits.get_ber()
            print "Step", i + 1, "/", len(interferer_freq_css), ": BER at", interferer_freq_css[i]/1e6, "MHz:", ber
            ber_vals.append(ber)
            t_elapsed = time.time() - t0
            print "approximately", t_elapsed * (len(interferer_freq_css) - i - 1) / 60, "minutes remaining"
            np.save("tmp_ber_singletone_css_" + str(min(interferer_freq_css/1e6)) + "_to_" + str(
                max(interferer_freq_css/1e6)) + "MHz", ber_vals)

        name = "ber_singletone_css_slow-rate-" + str(tb.c.slow_rate) + "_" + str(min(interferer_freq_css/1e6)) + "_to_" + str(
            max(interferer_freq_css/1e6)) + "MHz_" + time.strftime("%Y-%m-%d_%H-%M-%S")
        np.save(name, ber_vals)
        try:
            plt.plot(interferer_freq_css, ber_vals, label="SIR=" + str(snr_vals) + " dB")
            plt.legend(loc='lower left')
            plt.xlabel("Frequency [Hz]")
            plt.xlim([-fs_css/2, fs_css/2])
            plt.ylabel("BER")
            plt.grid()
            plt.yscale('log')
            plt.title(name)
            plt.savefig(name + ".pdf")
            plt.clear()
        except:
            print "plotting CSS fast curves failed"
            pass

    if en_css_slow:
        # CSS fast
        if min_len <= 1e3:
            print "WARNING: min_len very short:", min_len
        print "Collect", min_len, "bytes per step"
        old_len_res = 0
        ber_vals = []
        for i in range(len(interferer_freq_css)):
            t0 = time.time()
            tb = None
            gc.collect()
            tb = ber_singletone_css(cfg_slow)
            tb.set_snr(snr_vals)
            tb.singletone_src.set_frequency(interferer_freq_css[i])
            tb.start()
            time.sleep(.1)
            ber = 1.0
            while (True):
                len_res = tb.comp_bits.get_bits_compared()
                print interferer_freq_css[i]/1000000, "MHz:", 100.0 * len_res / min_len, "% done"
                if (len_res >= min_len):
                    if (tb.comp_bits.get_errors_found() >= min_err or tb.comp_bits.get_bits_compared() >= 10 * min_len):
                        print "Found a total of", tb.comp_bits.get_errors_found(), " errors"
                        tb.stop()
                        break
                    else:
                        print "Found", tb.comp_bits.get_errors_found(), "of", min_err, "errors"
                if (ber == 0 ):
                    tb.stop()
                    tb.wait()
                    time.sleep(.1)
                    break
                time.sleep(sleeptime)
                old_len_res = len_res

            ber = tb.comp_bits.get_ber()
            print "Step", i + 1, "/", len(interferer_freq_css), ": BER at", interferer_freq_css[i]/1e6, "MHz:", ber
            ber_vals.append(ber)
            t_elapsed = time.time() - t0
            print "approximately", t_elapsed * (len(interferer_freq_css) - i - 1) / 60, "minutes remaining"
            np.save("tmp_ber_singletone_css_" + str(min(interferer_freq_css/1e6)) + "_to_" + str(
                max(interferer_freq_css/1e6)) + "MHz", ber_vals)
            del tb

        name = "ber_singletone_css_slow-rate-" + str(tb.c.slow_rate) + "_" + str(min(interferer_freq_css/1e6)) + "_to_" + str(
            max(interferer_freq_css/1e6)) + "MHz_" + time.strftime("%Y-%m-%d_%H-%M-%S")
        np.save(name, ber_vals)
        try:
            plt.plot(interferer_freq_css, ber_vals, label="SIR=" + str(snr_vals) + " dB")
            plt.legend(loc='lower left')
            plt.xlabel("Frequency [Hz]")
            plt.xlim([-fs_css/2, fs_css/2])
            plt.ylabel("BER")
            plt.grid()
            plt.yscale('log')
            plt.title(name)
            plt.savefig(name + ".pdf")
            plt.clear()
        except:
            print "plotting CSS slow curve failed"
            pass
