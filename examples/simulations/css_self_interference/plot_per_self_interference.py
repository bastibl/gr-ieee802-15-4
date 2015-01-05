#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import time
if __name__ == "__main__":
    css_slow_short = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/css_self_interference/results/per_self_interference_css_slow_rate-True_packet-len-12bytes_-25.0_to_-5.5dB_2014-12-21_22-02-11.npy")
    css_slow_long = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/css_self_interference/results/per_self_interference_css_slow_rate-True_packet-len-127bytes_-25.0_to_-5.5dB.npy")
    css_fast_short = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/css_self_interference/results/per_self_interference_css_slow_rate-False_packet-len-12bytes_-20.0_to_-0.5dB_2014-12-20_23-16-07.npy")
    css_fast_long = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/css_self_interference/results/per_self_interference_css_slow_rate-False_packet-len-127bytes_-20.0_to_-0.5dB_2014-12-20_18-21-54.npy")
    snr_slow = np.arange(-25.0,-5.0,.5)
    snr_fast = np.arange(-20.0,0.0,.5)

    plt.rcParams.update({'font.size': 16})
    plt.rcParams.update({'axes.labelsize': 'large'})
    xlow = 0.0
    xhigh = 12.5
    ylow = 1e-3
    yhigh = 1

    # Eb/N0 plot
    EbN0_fast = snr_fast + 10*np.log10(32e6/1e6)
    EbN0_slow = snr_slow + 10*np.log10(32e6/250e3)

    f1 = plt.figure(1)
    m = ['o', 'v', 's', 'x']
    for i in range(4):
        plt.plot(EbN0_fast, css_fast_short[i,:], label="# interferer: "+str(i), marker = m[i])
    plt.grid()
    # plt.title("CSS PHY Self-Interference (1 Mbps)")
    plt.legend(loc = 'lower left')
    plt.xlabel("Eb/N0")
    plt.ylabel("PER")
    plt.yscale('log')
    plt.xlim([xlow, xhigh])
    plt.ylim([ylow, yhigh])
    plt.savefig("per_css_fast_short_self_interference.pdf")

    f2 = plt.figure(2)
    m = ['o', 'v', 's', 'x']
    for i in range(4):
        plt.plot(EbN0_fast, css_fast_long[i,:], label="# interferer: "+str(i), marker = m[i])
    plt.grid()
    # plt.title("CSS PHY Self-Interference (1 Mbps)")
    plt.legend(loc = 'lower left')
    plt.xlabel("Eb/N0")
    plt.ylabel("PER")
    plt.yscale('log')
    plt.xlim([xlow, xhigh])
    plt.ylim([ylow, yhigh])
    plt.savefig("per_css_fast_long_self_interference.pdf")

    f3 = plt.figure(3)
    for i in range(4):
        plt.plot(EbN0_slow, css_slow_short[i,:], label="# interferer: "+str(i), marker=m[i])
    plt.grid()
    # plt.title("CSS PHY Self-Interference (250 kbps)")
    plt.legend(loc = 'lower left')
    plt.xlabel("Eb/N0")
    plt.ylabel("PER")
    plt.yscale('log')
    plt.ylim([ylow, yhigh])
    plt.xlim([xlow, xhigh])
    plt.savefig("per_css_slow_short_self_interference.pdf")

    f4 = plt.figure(4)
    for i in range(4):
        plt.plot(EbN0_slow, css_slow_long[i,:], label="# interferer: "+str(i), marker=m[i])
    plt.grid()
    # plt.title("CSS PHY Self-Interference (250 kbps)")
    plt.legend(loc = 'lower left')
    plt.xlabel("Eb/N0")
    plt.ylabel("PER")
    plt.yscale('log')
    plt.ylim([ylow, yhigh])
    plt.xlim([xlow, xhigh])
    plt.savefig("per_css_slow_long_self_interference.pdf")