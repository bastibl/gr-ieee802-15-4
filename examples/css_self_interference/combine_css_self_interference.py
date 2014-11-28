__author__ = 'wunsch'

#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    css_slow = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/css_self_interference/ber_self_interference_css_slow_rate-True_-30.0_to_-11.0dB_2014-11-28_12-09-38.npy")
    css_fast = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/css_self_interference/ber_self_interference_css_slow_rate-False_-25.0_to_-1.0dB_2014-11-28_12-55-02.npy")
    snr_slow = np.arange(-30.0,-10.0,1.0)
    snr_fast = np.arange(-25.0,0.0,1.0)

    f, axarr = plt.subplots(2)
    for i in range(4):
        axarr[0].plot(snr_fast, css_fast[i,:], label="# interferer: "+str(i))
    axarr[0].grid()
    axarr[0].set_title("Fast mode (1 Mbps)")
    axarr[0].legend(loc = 'lower left')
    axarr[0].set_xlabel("SNR")
    axarr[0].set_ylabel("BER")
    axarr[0].set_yscale('log')

    for i in range(4):
        print len(snr_slow), len(css_slow[i,:])
        axarr[1].plot(snr_slow, css_slow[i,:], label="# interferer: "+str(i))
    axarr[1].grid()
    axarr[1].set_title("Slow mode (250 kbps)")
    axarr[1].legend(loc = 'lower left')
    axarr[1].set_xlabel("SNR")
    axarr[1].set_ylabel("BER")
    axarr[1].set_yscale('log')
    axarr[1].set_ylim([1e-5,1])

    plt.suptitle("Influence of self-interference in multi-user scenarios with AWGN")

    plt.show()
