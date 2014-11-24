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
noise_ampl_vals = np.arange(-4.0,-3.5,1.0)
nbytes_per_frame = 127
cfg = ieee802_15_4.css_phy(slow_rate=True, phy_packetsize_bytes=nbytes_per_frame)
min_err = 100
min_ber = 0.00001
min_len = int(min_err/min_ber)
nframes = float(min_len)/nbytes_per_frame
nsamps_frame = 4*8*(4+1+1+nbytes_per_frame)
nsamps_total = nframes*nsamps_frame
pdp = [np.exp(-21586735.0*tau) for tau in np.arange(0.0,320*1e-9, 1.0/(4*1e6))]
if len(pdp) % 2 == 0:
    pdp.append(0)
coherence_time_samps = nsamps_frame*10

class ber_rayleigh_comp_nogui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "BER AWGN Test OQPSK")

        ##################################################
        # Variables
        ##################################################
        self.noise_ampl = noise_ampl = 0
        self.c = c = cfg

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_15_4_oqpsk_phy_nosync_0 = ieee802_15_4_oqpsk_phy_nosync(
            payload_len=c.phy_packetsize_bytes,
        )
        self.ieee802_15_4_rayleigh_channel_sim = ieee802_15_4.rayleigh_multipath_cc(pdp, coherence_time_samps)
        self.skip_fir_group_delay = blocks.skiphead(gr.sizeof_gr_complex, (len(pdp)-1)/2)
        self.ieee802_15_4_make_pair_with_blob_0 = ieee802_15_4.make_pair_with_blob(np.random.randint(0,256,(c.phy_packetsize_bytes,)))
        self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol("trigger")), 1, 5, True, False)
        self.comp_bits = ieee802_15_4.compare_blobs(packet_error_mode=False)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 10**(-noise_ampl/10), 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_add_xx_0_0, 0), (self.ieee802_15_4_oqpsk_phy_nosync_0, 0))
        self.connect(self.ieee802_15_4_oqpsk_phy_nosync_0, self.ieee802_15_4_rayleigh_channel_sim)
        self.connect(self.skip_fir_group_delay, (self.blocks_add_xx_0_0, 0))
        self.connect(self.ieee802_15_4_rayleigh_channel_sim, self.skip_fir_group_delay)

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.ieee802_15_4_oqpsk_phy_nosync_0, "txin")
        self.msg_connect(self.foo_periodic_msg_source_0, "out", self.ieee802_15_4_make_pair_with_blob_0, "in")
        # self.msg_connect(self.msg_trigger, "strobe", self.ieee802_15_4_make_pair_with_blob_0, "in")
        self.msg_connect(self.ieee802_15_4_make_pair_with_blob_0, "out", self.comp_bits, "ref")
        self.msg_connect(self.ieee802_15_4_oqpsk_phy_nosync_0, "rxout", self.comp_bits, "test")
        self.msg_connect(self.ieee802_15_4_oqpsk_phy_nosync_0, "rxout", self.ieee802_15_4_make_pair_with_blob_0, "in")

    def get_noise_ampl(self):
        return self.noise_ampl

    def set_noise_ampl(self, noise_ampl):
        self.noise_ampl = noise_ampl
        self.analog_noise_source_x_0_0.set_amplitude(10**(-self.noise_ampl/10))

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
    
    print "The channel changes a total of", nsamps_total/coherence_time_samps, "times every", float(coherence_time_samps)/cfg.nsamp_frame, "frames"

    if min_len <= 1e3:
        raise Exception("min_len too short")
    min_ram_usage_mb = 2.0*min_len/1024/1024
    print "Simulation needs at least", min_ram_usage_mb, "MB of RAM"
    if min_ram_usage_mb > 4000:
        print "Careful, simulation needs more than 4GB RAM!"
    print "Simulate from", min(noise_ampl_vals), "to", max(noise_ampl_vals), "dB SNR"
    print "Collect",min_len,"bytes per step"
    ber_vals = [];
    n_channels = 1000;
    for i in range(len(noise_ampl_vals)):
        t0 = time.time()
        tb = None
        tb = ber_rayleigh_comp_nogui()
        tb.set_noise_ampl(noise_ampl_vals[i])
        tb.start()
        while(True):
            len_res = tb.comp_bits.get_bits_compared()
            print noise_ampl_vals[i], "dB:", 100.0*len_res/min_len, "% done"
            time.sleep(1)
            if(len_res >= min_len):
                tb.stop()
                break

        ber = tb.comp_bits.get_ber()
        print "BER at", noise_ampl_vals[i], "dB SNR: ", ber
        ber_vals.append(ber)
        t_elapsed = time.time() - t0
        print "approximately",t_elapsed*(len(noise_ampl_vals)-len(ber_vals))/60, "minutes remaining"

    np.save("ber_rayleigh_oqpsk_"+str(min(noise_ampl_vals))+"_to_"+str(max(noise_ampl_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"), ber_vals)
    plt.plot(noise_ampl_vals, ber_vals)
    plt.yscale('log')
    plt.title("ber_rayleigh_oqpsk_"+str(min(noise_ampl_vals))+"_to_"+str(max(noise_ampl_vals))+"dB_"+time.strftime("%Y-%m-%d_%H-%M-%S"))
    plt.show()


