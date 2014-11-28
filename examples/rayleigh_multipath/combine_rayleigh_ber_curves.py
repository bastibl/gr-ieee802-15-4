#! /usr/bin/env python
__author__ = 'wunsch'
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    oqpsk = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_oqpsk_-30.0_to_4.0dB_2014-11-26_17-30-23.npy")
    css_fast = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_css_sd_slow_rate-False_-25.0_to_9.0dB_2014-11-28_10-07-50.npy")
    css_slow = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_css_sd_slow_rate-True_-25.0_to_-2.0dB.npy")
    snr_css_fast = np.arange(-25.0, 10.0, 1.0)
    snr_css_slow = np.arange(-25.0, -1.0, 1.0)
    snr_oqpsk = np.arange(-30.0, 5.0, 1.0)

    t =  np.arange(0.0, 320 * 1e-9, 1.0 / (32 * 1e6))
    pdp = [np.exp(-28782313.0 * tau) for tau in t]
    if len(pdp) % 2 == 0:
        pdp.append(0)
    for i in range(len(pdp)):
        if i%8 != 0:
            pdp[i] = 0
    print pdp

    f, axarr = plt.subplots(2)

    axarr[1].plot(snr_oqpsk, oqpsk, label="OQPSK")
    axarr[1].plot(snr_css_fast, css_fast, label="CSS 1 Mbps (SD)")
    axarr[1].plot(snr_css_slow, css_slow, label="CSS 250 kbps (SD)")
    axarr[1].legend(loc='lower left')
    axarr[1].grid()
    axarr[1].set_yscale('log')
    axarr[1].set_xlabel("SNR")
    # axarr[1].set_xlim([-25,-3])
    axarr[1].set_ylabel("BER")
    axarr[1].set_title("Bit error rates in Rayleigh channel with AWGN")

    markerline, stemlines, baseline = axarr[0].stem(t*1e9, pdp, '-', bottom=0.00001)
    axarr[0].set_xlabel("delay in ns")
    axarr[0].set_xlim([-10, max(t)*1e9])
    axarr[0].set_ylabel("normalized power")
    axarr[0].grid()
    axarr[0].set_ylim([0.0001,8])
    axarr[0].set_title("Power delay profile")
    axarr[0].set_yscale('log')
    plt.savefig("ber_rayleigh_combined_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")
    plt.show()

