#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    oqpsk = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_100kHz_oqpsk_-20.0_to_-0.5dB_2014-12-04_15-38-54.npy")
    sir_oqpsk = np.arange(-20.0,-0.0, .5)
    css_fast = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_100kHz_css_sd_slow_rate-False_-15.0_to_-0.5dB_2014-12-04_15-52-38.npy")
    sir_css_fast = np.arange(-15.0, -0.0, .5)
    css_slow = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/singletone_interferer/ber_singletone_100kHz_css_sd_slow_rate-True_-15.0_to_-0.5dB_2014-12-04_16-29-42.npy")
    sir_css_slow = np.arange(-15.0, 0.0, .5)

    plt.plot(sir_css_slow, css_slow[0:len(sir_css_slow)], label="CSS 250 kbps")
    plt.plot(sir_css_fast, css_fast, label="CSS 1 Mbps")
    plt.plot(sir_oqpsk, oqpsk, label="OQPSK")
    plt.legend(loc='lower left')
    plt.xlabel("SIR")
    plt.xlim([-15,-5.25])
    plt.ylim([1e-5, 1])
    plt.ylabel("BER")
    plt.title("BER with Single-tone Interferer at 100 kHz")
    plt.grid()
    plt.yscale('log')
    plt.savefig("ber_sir_singletone_combined_"+time.strftime("%Y-%m-%d_%H-%M-%S")+".pdf")
    plt.show()

