#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    # oqpsk = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_oqpsk_-15.0_to_-3.5dB.npy")
    oqpsk = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_100kHz_oqpsk_-15.0_to_-5.25dB_2014-12-02_15-24-23.npy")
    sir_oqpsk = np.arange(-15.0,-5.0, .25)
    # css_fast = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/singletone_interferer/tmp_ber_singletone_100.0Hz_css_sd_slow_rate-False_-20.0_to_-0.5dB.npy")
    css_fast = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_100kHz_css_sd_slow_rate-False_-15.0_to_-5.25dB_2014-12-02_14-01-37.npy")
    sir_css_fast = np.arange(-15.0, -5.0, .25)
    # css_slow = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_100kHz_css_sd_slow_rate-True_-20.0_to_-0.25dB_2014-11-30_12-56-28.npy")
    css_slow = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_100kHz_css_sd_slow_rate-True_-15.0_to_-5.25dB_2014-12-02_13-43-43.npy")
    sir_css_slow = np.arange(-15.0, -9.25, .25)

    plt.plot(sir_oqpsk, oqpsk, label="OQPSK")
    plt.plot(sir_css_fast, css_fast, label="CSS 1 Mbps")
    plt.plot(sir_css_slow, css_slow[0:len(sir_css_slow)], label="CSS 250 kbps")
    plt.legend(loc='lower left')
    plt.xlabel("SIR")
    plt.xlim([-15,-5.25])
    plt.ylabel("BER")
    plt.title("BER with single-tone interferer at 100 kHz")
    plt.grid()
    plt.yscale('log')
    plt.savefig("ber_sir_singletone_combined_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")
    plt.show()

