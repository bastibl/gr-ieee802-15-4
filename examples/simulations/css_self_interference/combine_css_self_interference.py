__author__ = 'wunsch'

#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import time
if __name__ == "__main__":
    css_slow = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/css_self_interference/ber_self_interference_css_slow_rate-True_-25.0_to_-10.5dB_2014-12-03_15-48-06.npy")
    css_fast = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/css_self_interference/ber_self_interference_css_slow_rate-False_-25.0_to_-5.5dB_2014-12-03_14-07-00.npy")
    snr_slow = np.arange(-25.0,-10.0,.5)
    snr_fast = np.arange(-25.0,-5.0,.5)

    plt.rcParams.update({'font.size': 16})
    plt.rcParams.update({'axes.labelsize': 'large'})
    plt.rcParams.update({'axes.labelsize': 'large'})

    # Eb/N0 plot
    Eb_noSF = 19.0007 # sum(|norm_fac*chirp_seq|^2)/8 --> Energy per code bit
    Eb_slow = Eb_noSF*32.0/6
    Eb_fast = Eb_noSF*4.0/3
    # this Eb/N0 does not consider energy spent on headers, only the payload including the respective coding rate is considered because otherwise the number of payload bytes per frame would gain influence
    EbN0_fast = 10*np.log10(Eb_fast) + snr_fast
    EbN0_slow = 10*np.log10(Eb_slow) + snr_slow

    f = plt.figure(1)
    m = ['o', 'v', 's', 'x']
    for i in range(4):
        plt.plot(EbN0_fast, css_fast[i,:], label="# interferer: "+str(i), marker = m[i])
    plt.grid()
    # plt.title("CSS PHY Self-Interference (1 Mbps)")
    plt.legend(loc = 'lower left')
    plt.xlabel("Eb/N0")
    plt.ylabel("BER")
    plt.yscale('log')
    plt.xlim([-11,8])
    plt.ylim([3e-5,1])
    plt.savefig("css_fast_self_interference.pdf")

    f2 = plt.figure(2)
    for i in range(4):
        print len(snr_slow), len(css_slow[i,:])
        plt.plot(EbN0_slow, css_slow[i,:], label="# interferer: "+str(i), marker=m[i])
    plt.grid()
    # plt.title("CSS PHY Self-Interference (250 kbps)")
    plt.legend(loc = 'lower left')
    plt.xlabel("Eb/N0")
    plt.ylabel("BER")
    plt.yscale('log')
    plt.ylim([3e-5,1])
    plt.xlim([-5,9.5])

    plt.savefig("css_slow_self_interference.pdf")

