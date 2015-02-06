#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

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
    ber_css_slow = np.load("")
    ber_css_fast = np.load("")
    ber_oqpsk = np.load("h")
    snr_slow = np.arange(-25.0, -10.0, .5)
    snr_fast = np.arange(-25.0, -5.0, .5)
    fs = 32e6
    rate_slow = 250e3
    rate_fast = 1e6

    nbytes_short_PSDU = 5
    nbytes_short_packet = nbytes_short_PSDU + 7.0/8 # + PHR
    nbytes_long_PSDU = 127
    nbytes_long_packet = nbytes_long_PSDU + 7.0/8 # + PHR
    m = ['o', 'v', 's', 'x']
    c = ['b', 'g', 'r', 'c']

    plt.rcParams.update({'font.size': 10})
    plt.rcParams.update({'axes.labelsize': 'large'})

    f1 = plt.figure(1)
    for i in range(4):
        plt.semilogy(calc_ebn0(snr_fast, rate_fast, fs), calc_per(ber_css_fast[i,:], nbytes_short_packet), label=str(nbytes_short_PSDU)+" byte PSDU, "+ str(i) + " interferer(s)", marker = m[i], color = c[i], linestyle = '-')

    for i in range(4):
        plt.semilogy(calc_ebn0(snr_fast, rate_fast, fs), calc_per(ber_css_fast[i,:], nbytes_long_packet), label=str(nbytes_long_packet)+" byte with "+ str(i) + " interferer(s)", marker = m[i], color = c[i], linestyle = '--')

    plt.grid()
    plt.legend(loc='lower left')
    plt.xlim([0,9.5])
    plt.ylim([5e-3, 2])
    plt.ylabel("PER")
    plt.xlabel("Eb/N0 [dB]")

    plt.savefig("per_calc_singletone_interferer.pdf", bbox='tight')

    plt.show()
