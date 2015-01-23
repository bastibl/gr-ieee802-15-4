#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    oqpsk = np.load("results/ber_singletone_100kHz_oqpsk_-20.0_to_-0.5dB_2015-01-05_20-16-36.npy")
    sir_oqpsk = np.arange(-20.0,-0.0, .5)
    css_fast = np.load("results/ber_singletone_1800kHz_css_sd_slow_rate-False_-15.0_to_4.5dB_2015-01-05_18-19-35.npy")
    sir_css_fast = np.arange(-15.0, 5.0, .5)
    css_slow = np.load("results/ber_singletone_1800kHz_css_sd_slow_rate-True_-15.0_to_-0.5dB_2015-01-05_16-57-32.npy")
    sir_css_slow = np.arange(-15.0, 0.0, .5)

    plt.rcParams.update({'font.size': 18})
    plt.rcParams.update({'axes.labelsize': 'large'})
    plt.rcParams.update({'axes.labelsize': 'large'})

    f1 = plt.figure(1)
    plt.plot(sir_css_slow, css_slow[0:len(sir_css_slow)], label="CSS 250 kb/s", marker='o')
    plt.plot(sir_css_fast, css_fast, label="CSS 1 Mb/s", marker='v')
    # plt.plot(sir_oqpsk, oqpsk, label="OQPSK", marker='s')
    plt.legend(loc='lower left')
    plt.xlabel("SIR [dB]")
    plt.xlim([-15,3])
    plt.ylim([1e-3, 1])
    plt.ylabel("BER")
    plt.grid()
    plt.yscale('log')
    plt.savefig("ber_sir_singletone_css.pdf",bbox='tight')

    f2 = plt.figure(2)
    plt.plot(sir_oqpsk, oqpsk, label="OQPSK", marker='s', c='r')
    plt.legend(loc='lower left')
    plt.xlabel("SIR [dB]")
    plt.xlim([-15,3])
    plt.ylim([6e-3, 1])
    plt.ylabel("BER")
    plt.grid()
    plt.yscale('log')
    plt.savefig("ber_sir_singletone_oqpsk.pdf",bbox='tight')

    plt.show()
