__author__ = 'wunsch'

#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import time
if __name__ == "__main__":
    css_slow = np.load("")
    css_fast = np.load("")
    snr_slow = np.arange(-25.0,-10.0,.5)
    snr_fast = np.arange(-25.0,-5.0,.5)

    plt.rcParams.update({'font.size': 16})
    plt.rcParams.update({'axes.labelsize': 'large'})
    plt.rcParams.update({'axes.labelsize': 'large'})

    # Eb/N0 plot
    EbN0_fast = snr_fast + 10*np.log10(32e6/1e6)
    EbN0_slow = snr_slow + 10*np.log10(32e6/250e3)

    f = plt.figure(1)
    m = ['o', 'v', 's', 'x']
    for i in range(4):
        plt.plot(EbN0_fast, css_fast[i,:], label="# interferer: "+str(i), marker = m[i])
    plt.grid()
    # plt.title("CSS PHY Self-Interference (1 Mbps)")
    plt.legend(loc = 'lower left')
    plt.xlabel("Eb/N0")
    plt.ylabel("PER")
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
    plt.ylabel("PER")
    plt.yscale('log')
    plt.ylim([3e-5,1])
    plt.xlim([-5,9.5])

    plt.savefig("css_slow_self_interference.pdf")

