#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: BER AWGN Test CSS SD/HD vs OQPSK
# Author: Felix Wunsch
# Generated: Mon Nov 10 19:00:50 2014
##################################################

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
snr_vals = np.arange(-15.0, -5.0, .25)
nbytes_per_frame = 127
min_err = int(1e3)
min_len = int(1e8)
msg_interval = 1  # ms
sleeptime = 1.0  # s
interferer_freq = 100e3
fs = 4e6


class ber_singletone_nogui(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "BER CSS with singletone interferer")

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
        self.singletone_src = analog.sig_source_c(fs, analog.GR_COS_WAVE, interferer_freq, 10 ** (-snr / 20))
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


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."

    if min_len <= 1e3:
        print "WARNING: min_len very short:", min_len
    print "Simulate from", min(snr_vals), "to", max(snr_vals), "dB snr"
    print "Collect", min_len, "bytes per step"
    old_len_res = 0
    ber_vals = []
    for i in range(len(snr_vals)):
        t0 = time.time()
        tb = None
        tb = ber_singletone_nogui()
        tb.set_snr(snr_vals[i])
        tb.start()
        time.sleep(.1)
        ber = 1.0
        while (True):
            len_res = tb.comp_bits.get_bits_compared()
            print snr_vals[i], "dB:", 100.0 * len_res / min_len, "% done"
            if (len_res >= min_len):
                if (tb.comp_bits.get_errors_found() >= min_err or tb.comp_bits.get_bits_compared() >= 10 * min_len or tb.comp_bits.get_errors_found() == 0):
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
        print "Step", i + 1, "/", len(snr_vals), ": BER at", snr_vals[i], "dB snr:", ber
        ber_vals.append(ber)
        t_elapsed = time.time() - t0
        print "approximately", t_elapsed * (len(snr_vals) - i - 1) / 60, "minutes remaining"
        np.save("tmp_ber_singletone_oqpsk_" + str(min(snr_vals)) + "_to_" + str(
            max(snr_vals)) + "dB", ber_vals)

    name = "ber_singletone_" + str(int(interferer_freq / 1000)) + "kHz_oqpsk_" + str(min(snr_vals)) + "_to_" + str(
        max(snr_vals)) + "dB_" + time.strftime("%Y-%m-%d_%H-%M-%S")
    np.save(name, ber_vals)
    plt.plot(snr_vals, ber_vals, label="single-tone interferer frequency: " + str(int(interferer_freq / 1000)) + " kHz")
    plt.legend(loc='lower left')
    plt.xlabel("SIR")
    plt.ylabel("BER")
    plt.grid()
    plt.yscale('log')
    plt.title(name)
    plt.savefig(name + ".pdf")
    plt.show()
