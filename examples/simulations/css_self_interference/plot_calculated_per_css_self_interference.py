#! /usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

def calc_per(ber, bytes_per_packet):
    if np.isscalar(ber):
        return 1-(1-ber)**(8*bytes_per_packet)
    else:
        return [1-(1-p)**(8*bytes_per_packet) for p in ber]

def calc_ebn0(snr, rate, bw):
    fac = 10*np.log10(float(bw)/rate)
    if np.isscalar(snr):
        return snr + fac
    else:
        return [snr_val + fac for snr_val in snr]



if __name__ == "__main__":
    ber_css_slow = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/css_self_interference/results/ber_self_interference_css_slow_rate-True_-25.0_to_-10.5dB_2014-12-03_15-48-06.npy")
    ber_css_fast = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/css_self_interference/results/ber_self_interference_css_slow_rate-False_-25.0_to_-5.5dB_2014-12-03_14-07-00.npy")
    snr_slow = np.arange(-25.0, -10.0, .5)
    snr_fast = np.arange(-25.0, -5.0, .5)
    fs = 32e6
    rate_slow = 250e3
    rate_fast = 1e6

    nbytes_short_packet = 5
    nbytes_long_packet = 127
    m = ['o', 'v', 's', 'x']
    c = ['b', 'g', 'r', 'c']

    f1 = plt.figure(1)
    for i in range(4):
        plt.semilogy(calc_ebn0(snr_fast, rate_fast, fs), calc_per(ber_css_fast[i,:], nbytes_short_packet), label=str(nbytes_short_packet)+" byte with "+ str(i) + " interferer(s)", marker = m[i], color = c[i], linestyle = '-')

    for i in range(4):
        plt.semilogy(calc_ebn0(snr_fast, rate_fast, fs), calc_per(ber_css_fast[i,:], nbytes_long_packet), label=str(nbytes_long_packet)+" byte with "+ str(i) + " interferer(s)", marker = m[i], color = c[i], linestyle = '--')

    plt.grid()
    plt.legend(loc='lower left')
    plt.xlim([0,9.5])
    plt.ylim([5e-3, 2])
    plt.ylabel("PER")
    plt.xlabel("Eb/N0")

    plt.savefig("per_calc_css_fast_self_interference.pdf", bbox='tight')

    f2 = plt.figure(2)
    for i in range(4):
        plt.semilogy(calc_ebn0(snr_slow, rate_slow, fs), calc_per(ber_css_slow[i,:], nbytes_short_packet), label=str(nbytes_short_packet)+" byte with "+ str(i) + " interferer(s)", marker = m[i], color = c[i], linestyle = '-')

    for i in range(4):
        plt.semilogy(calc_ebn0(snr_slow, rate_slow, fs), calc_per(ber_css_slow[i,:], nbytes_long_packet), label=str(nbytes_long_packet)+" byte with "+ str(i) + " interferer(s)", marker = m[i], color = c[i], linestyle = '--')

    plt.grid()
    plt.legend(loc='lower left')
    plt.xlim([0,9.5])
    plt.ylim([5e-3, 2])
    plt.ylabel("PER")
    plt.xlabel("Eb/N0")

    plt.savefig("per_calc_css_slow_self_interference.pdf", bbox='tight')

    plt.show()
