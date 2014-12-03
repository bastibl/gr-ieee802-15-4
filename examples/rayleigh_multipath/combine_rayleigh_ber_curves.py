#! /usr/bin/env python
__author__ = 'wunsch'
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    oqpsk1 = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_oqpsk_-30.0_to_4.0dB_2014-11-26_17-30-23.npy")
    oqpsk2 = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_oqpsk_5.0_to_14.0dB_2014-12-02_12-27-03.npy")
    oqpsk = np.concatenate((oqpsk1, oqpsk2))
    css_fast1 = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_css_sd_slow_rate-False_-25.0_to_9.0dB_2014-11-28_10-07-50.npy")
    css_fast2 = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_css_sd_slow_rate-False_10.0_to_14.0dB_2014-12-02_12-08-04.npy")
    css_fast = np.concatenate((css_fast1, css_fast2))
    #css_slow1 = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_css_sd_slow_rate-True_-25.0_to_-2.0dB.npy")
    css_slow1 = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_css_sd_slow_rate-True_-25.0_to_-1.0dB_2014-12-02_11-57-04.npy")
    css_slow2 = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/rayleigh_multipath/ber_rayleigh_css_sd_slow_rate-True_0.0_to_5.0dB_2014-12-02_10-40-24.npy")
    css_slow = np.concatenate((css_slow1, css_slow2))
    snr_css_fast = np.arange(-25.0, 15.0, 1.0)
    snr_css_slow = np.arange(-25.0, 6.0, 1.0)
    snr_oqpsk = np.arange(-30.0, 15.0, 1.0)

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
    # axarr[1].plot(snr_oqpsk, oqpsk, label="OQPSK")
    # axarr[1].plot(snr_css_fast, css_fast, label="CSS 1 Mbps (SD)")
    # axarr[1].plot(snr_css_slow, css_slow, label="CSS 250 kbps (SD)")
    # axarr[1].legend(loc='lower left')
    # axarr[1].grid()
    # axarr[1].set_yscale('log')
    # axarr[1].set_xlabel("SNR")
    # # axarr[1].set_xlim([-25,-3])
    # axarr[1].set_ylabel("BER")
    # axarr[1].set_title("Bit error rates in Rayleigh channel with AWGN")
    #
    # markerline, stemlines, baseline = axarr[0].stem(t*1e9, pdp, '-', bottom=0.00001)
    # axarr[0].set_xlabel("delay in ns")
    # axarr[0].set_xlim([-10, max(t)*1e9])
    # axarr[0].set_ylabel("normalized power")
    # axarr[0].grid()
    # axarr[0].set_ylim([0.0001,8])
    # axarr[0].set_title("Power delay profile")
    # axarr[0].set_yscale('log')
    # plt.savefig("ber_rayleigh_SNR_combined_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")
    # plt.show()

    # EbN0 plots
    f, axarr = plt.subplots(2)
    css_Eb_noSF = 19.0007 # sum(|norm_fac*chirp_seq|^2)/8 --> Energy per code bit
    css_slow_Eb = css_Eb_noSF*32.0/6
    css_fast_Eb = css_Eb_noSF*4.0/3
    # this Eb/N0 does not consider energy spent on headers, only the payload including the respective coding rate is considered because otherwise the number of payload bytes per frame would gain influence
    css_fast_EbN0 = 10*np.log10(css_fast_Eb) + snr_css_fast
    css_slow_EbN0 = 10*np.log10(css_slow_Eb) + snr_css_slow
    # OQPSK
    oqpsk_Eb = 64.0/4 # the OQPSK signal has always magnitude 1; one codeword is 64 samples long and encodes 4 payload bits (in the 2450 MHz band)
    oqpsk_EbN0 = 10*np.log10(oqpsk_Eb) + snr_oqpsk
    axarr[1].plot(oqpsk_EbN0, oqpsk, label="OQPSK")
    axarr[1].plot(css_fast_EbN0, css_fast, label="CSS 1 Mbps (SD)")
    axarr[1].plot(css_slow_EbN0, css_slow, label="CSS 250 kbps (SD)")
    axarr[1].legend(loc='lower left')
    axarr[1].grid()
    axarr[1].set_yscale('log')
    axarr[1].set_xlim([-5, 25])
    axarr[1].set_xlabel("Eb/N0")
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
    plt.savefig("ber_rayleigh_EbN0_combined_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")
    plt.show()

