#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    oqpsk = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_oqpsk_-15.0_to_-3.5dB.npy")
    sir_oqpsk = np.arange(-15.0,-3.0, .5)
    css_fast = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/singletone_interferer/tmp_ber_singletone_100.0Hz_css_sd_slow_rate-False_-20.0_to_-0.5dB.npy")
    sir_css_fast = np.arange(-20.0, 0, .5)
    css_slow = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_100kHz_css_sd_slow_rate-True_-20.0_to_-0.25dB_2014-11-30_12-56-28.npy")
    sir_css_slow = np.arange(-20.0, 0.0, .25)

    plt.plot(sir_oqpsk, oqpsk, label="OQPSK")
    plt.plot(sir_css_fast, css_fast, label="CSS 1 Mbps")
    plt.plot(sir_css_slow, css_slow, label="CSS 250 kbps")
    plt.legend(loc='lower left')
    plt.title("BER with single-tone interferer at 100 kHz")
    plt.grid()
    plt.yscale('log')
    plt.show()

    oqpsk2 = np.load("")
    sir_oqpsk2 = np.arange(-15.0,-3.0, .5)
    css_fast2 = np.load("")
    sir_css_fast2 = np.arange(-20.0, 0, .5)
    css_slow2 = np.load("")
    sir_css_slow2 = np.arange(-20.0, 0.0, .25)

    plt.plot(sir_oqpsk2, oqpsk2, label="OQPSK")
    plt.plot(sir_css_fast2, css_fast2, label="CSS 1 Mbps")
    plt.plot(sir_css_slow2, css_slow2, label="CSS 250 kbps")
    plt.legend(loc='lower left')
    plt.title("BER with single-tone interferer at 500 kHz")
    plt.grid()
    plt.yscale('log')
    plt.show()

