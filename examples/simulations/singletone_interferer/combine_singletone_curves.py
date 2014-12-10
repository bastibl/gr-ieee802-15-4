#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    oqpsk = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/singletone_interferer/ber_singletone_100kHz_oqpsk_-20.0_to_-0.5dB_2014-12-05_13-24-49.npy")
    sir_oqpsk = np.arange(-20.0,-0.0, .5)
    css_fast = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/singletone_interferer/ber_singletone_100kHz_css_sd_slow_rate-False_-15.0_to_-0.5dB_2014-12-05_14-30-35.npy")
    sir_css_fast = np.arange(-15.0, -0.0, .5)
    css_slow = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/singletone_interferer/ber_singletone_100kHz_css_sd_slow_rate-True_-15.0_to_-0.5dB_2014-12-05_15-34-21.npy")
    sir_css_slow = np.arange(-15.0, 0.0, .5)

    plt.rcParams.update({'font.size': 14})
    plt.rcParams.update({'axes.labelsize': 'large'})
    plt.rcParams.update({'axes.labelsize': 'large'})

    plt.plot(sir_css_slow, css_slow[0:len(sir_css_slow)], label="CSS 250 kb/s", marker='o')
    plt.plot(sir_css_fast, css_fast, label="CSS 1 Mb/s", marker='v')
    plt.plot(sir_oqpsk, oqpsk, label="OQPSK", marker='s')
    plt.legend(loc='lower left')
    plt.xlabel("SIR")
    plt.xlim([-15,-4])
    plt.ylim([1e-5, 1])
    plt.ylabel("BER")
    plt.grid()
    plt.yscale('log')
    plt.savefig("ber_sir_singletone_combined.pdf",bbox='tight')
    plt.show()

