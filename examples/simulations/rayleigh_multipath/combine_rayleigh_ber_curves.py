#! /usr/bin/env python
__author__ = 'wunsch'
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    # oqpsk = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_oqpsk_-25.0_to_14.0dB_2014-12-03_16-08-53.npy")
    oqpsk = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/simulations/rayleigh_multipath/ber_rayleigh_oqpsk_-25.0_to_14.0dB_2014-12-05_10-06-55.npy")
    css_fast = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/simulations/rayleigh_multipath/ber_rayleigh_css_sd_slow_rate-False_-25.0_to_14.0dB_2014-12-03_16-27-26.npy")
    css_slow = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/simulations/rayleigh_multipath/ber_rayleigh_css_sd_slow_rate-True_-25.0_to_14.0dB_2014-12-04_00-46-04.npy")
    snr_css_fast = np.arange(-25.0, 15.0, 1.0)
    snr_css_slow = np.arange(-25.0, 15.0, 1.0)
    snr_oqpsk = np.arange(-25.0, 15.0, 1.0)

    t =  np.arange(0.0, 320 * 1e-9, 1.0 / (32 * 1e6))
    pdp = [np.exp(-28782313.0 * tau) for tau in t]
    if len(pdp) % 2 == 0:
        pdp.append(0)
    for i in range(len(pdp)):
        if i%8 != 0:
            pdp[i] = 0
    print pdp


    # # SNR plots
    # f, axarr = plt.subplots(2)
    #
    # plt.plot(snr_oqpsk, oqpsk, label="OQPSK")
    # plt.plot(snr_css_fast, css_fast, label="CSS 1 Mbps (SD)")
    # plt.plot(snr_css_slow, css_slow, label="CSS 250 kbps (SD)")
    # plt.legend(loc='lower left')
    # plt.grid()
    # plt.set_yscale('log')
    # plt.set_xlabel("SNR")
    # # plt.set_xlim([-25,-3])
    # plt.set_ylabel("BER")
    # plt.set_title("Bit error rates in Rayleigh channel with AWGN")
    #
    # markerline, stemlines, baseline = plt.stem(t*1e9, pdp, '-', bottom=0.00001)
    # plt.set_xlabel("delay in ns")
    # plt.set_xlim([-10, max(t)*1e9])
    # plt.set_ylabel("normalized power")
    # plt.grid()
    # plt.set_ylim([0.0001,8])
    # plt.set_title("Power delay profile")
    # plt.set_yscale('log')
    # plt.savefig("ber_rayleigh_SNR_combined_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")
    # plt.show()

    # EbN0 plots
    f = plt.figure(1)
    # this Eb/N0 does not consider energy spent on headers, only the payload including the respective coding rate is considered because otherwise the number of payload bytes per frame would gain influence
    css_fast_EbN0 =snr_css_fast + 10*np.log10(32e6/1e6)
    css_slow_EbN0 = snr_css_slow + 10*np.log10(32e6/250e3)
    # OQPSK
    oqpsk_EbN0 = snr_oqpsk + 10*np.log10(4e6/250e3)
    plt.plot(css_slow_EbN0, css_slow, label="CSS 250 kbps (SD)")
    plt.plot(css_fast_EbN0, css_fast, label="CSS 1 Mbps (SD)")
    plt.plot(oqpsk_EbN0, oqpsk, label="OQPSK")
    plt.legend(loc='lower left')
    plt.grid()
    plt.yscale('log')
    plt.xlim([-5, 25])
    plt.xlabel("Eb/N0")
    plt.ylim([1e-6,1])
    plt.ylabel("BER")
    plt.title("Bit Error Rates in Rayleigh Channel with AWGN")
    plt.savefig("ber_rayleigh_EbN0_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")

    f2 = plt.figure(2)
    markerline, stemlines, baseline = plt.stem(t*1e9, pdp, '-', bottom=0.00001)
    plt.xlabel("Delay in ns")
    plt.xlim([-10, max(t)*1e9])
    plt.ylabel("Normalized Power")
    plt.grid()
    plt.ylim([0.0001,8])
    plt.title("Power delay profile")
    plt.yscale('log')
    plt.savefig("rayleigh_pdp_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")

