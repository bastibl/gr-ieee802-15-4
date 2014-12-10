#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: BER AWGN Test CSS SD/HD vs OQPSK
# Author: Felix Wunsch
# Generated: Mon Nov 10 19:00:50 2014
##################################################

execfile("/home/felixwunsch/.grc_gnuradio/ieee802_15_4_oqpsk_phy_nosync.py")
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
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
snr_vals = np.arange(-25.0,-0.0,1.0)
nbytes_per_frame = 127
min_err = int(1e3)
min_len = int(1e7)
nframes = float(min_len)/nbytes_per_frame
nsamps_frame = 4*8*(4+1+1+nbytes_per_frame)
nsamps_total = nframes*nsamps_frame
pdp = [np.exp(-28782313.0*tau) for tau in np.arange(0.0,320*1e-9, 1.0/(4e6))]
if len(pdp) % 2 == 0:
    pdp.append(0)
print "pdp:", pdp
group_delay = (len(pdp)-1)/2
coherence_time_samps = int(nsamps_frame*0.1)
coherence_time_samps = 1000#13670
sleeptime = 1.0
msg_interval = 50
skipsamps = 1 # simulates perfect sync

class ber_rayleigh_comp_nogui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "BER AWGN Test OQPSK")

        ##################################################
        # Variables
        ##################################################
        self.snr = snr = 0

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_15_4_oqpsk_phy_nosync_0 = ieee802_15_4_oqpsk_phy_nosync(
            payload_len=nbytes_per_frame,
        )
        self.ieee802_15_4_rayleigh_channel_sim = ieee802_15_4.rayleigh_multipath_cc(pdp, coherence_time_samps)
        self.skip_fir_group_delay = blocks.skiphead(gr.sizeof_gr_complex, skipsamps)
        self.ieee802_15_4_make_pair_with_blob_0 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(nbytes_per_frame,)))
        self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol("trigger")), 1, msg_interval, True, False)
        self.comp_bits = ieee802_15_4.compare_blobs(packet_error_mode=False)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.5*(10**(-snr/20)), 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect(self.ieee802_15_4_oqpsk_phy_nosync_0, self.ieee802_15_4_rayleigh_channel_sim)
        self.connect(self.ieee802_15_4_rayleigh_channel_sim, self.skip_fir_group_delay)
        self.connect(self.skip_fir_group_delay, (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.ieee802_15_4_oqpsk_phy_nosync_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_oqpsk_phy_nosync_0, "txin")
        self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0, "in")
        # self.msg_connect(self.msg_trigger, "strobe", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.comp_bits, "ref")
        self.msg_connect(self.ieee802_15_4_oqpsk_phy_nosync_0, "rxout", self.comp_bits, "test")
        self.msg_connect(self.ieee802_15_4_oqpsk_phy_nosync_0, "rxout", self.ieee802_15_4_make_pair_with_blob_0, "in")

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.analog_noise_source_x_0_0.set_amplitude(0.5 * (10 ** (-snr / 20)))

    def get_c(self):
        return self.c

    def set_c(self, c):
        self.c = c
        self.ieee802_15_4_oqpsk_phy_nosync_0.set_payload_len(self.c.phy_packetsize_bytes)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
    
    print "The channel changes a total of", nsamps_total/coherence_time_samps, "times every", float(coherence_time_samps)/nsamps_frame, "frames"

    if min_len <= 1e3:
        print "WARNING: min_len very short:", min_len
    min_ram_usage_mb = 2.0*min_len/1024/1024
    print "Simulation needs at least", min_ram_usage_mb, "MB of RAM"
    if min_ram_usage_mb > 4000:
        print "Careful, simulation needs more than 4GB RAM!"
    print "Simulate from", min(snr_vals), "to", max(snr_vals), "dB SNR"
    print "Collect",min_len,"bytes per step"
    ber_vals = [];
    for i in range(len(snr_vals)):
        t0 = time.time()
        tb = None
        tb = ber_rayleigh_comp_nogui()
        tb.set_snr(snr_vals[i])
        tb.start()
        while(True):
            len_res = tb.comp_bits.get_bits_compared()
            print snr_vals[i], "dB:", 100.0*len_res/min_len, "% of minimum length done"
            time.sleep(sleeptime)
            if(len_res >= min_len or tb.comp_bits.get_errors_found() >= min_err):
                if(tb.comp_bits.get_errors_found() >= min_err or tb.comp_bits.get_errors_found() == 0 or tb.comp_bits.get_bits_compared() >= 3*min_len):
                    print "Found a total of", tb.comp_bits.get_errors_found(), "errors"
                    tb.stop()
                    tb.wait()
                    break
                else:
                    print "Found", tb.comp_bits.get_errors_found(), "/", min_err, "errors"

        ber = tb.comp_bits.get_ber()
        print "Step", i+1, "/", len(snr_vals), ": BER at", snr_vals[i], "dB SNR: ", ber
        ber_vals.append(ber)
        t_elapsed = time.time() - t0
        print "approximately",t_elapsed*(len(snr_vals)-len(ber_vals))/60, "minutes remaining"

    np.save("ber_rayleigh_oqpsk_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"), ber_vals)
    plt.plot(snr_vals, ber_vals)
    plt.yscale('log')
    plt.xlabel("SNR")
    plt.ylabel("BER")
    plt.title("ber_rayleigh_oqpsk_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"))
    plt.grid()
    plt.savefig("ber_rayleigh_oqpsk_"+str(min(snr_vals))+"_to_"+str(max(snr_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".png")
    plt.show()


