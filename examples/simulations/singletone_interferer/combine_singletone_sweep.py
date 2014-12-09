#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    fs_oqpsk = 4e6
    fs_css = 32e6
    oqpsk = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/singletone_interferer/ber_singletone_oqpsk_-2.0_to_1.9MHz_2014-12-08_15-57-46.npy")
    css_slow = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/singletone_interferer/ber_singletone_css_slow-rate-True_-16.0_to_15.8MHz_2014-12-08_19-16-03.npy")
    css_fast = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/simulations/singletone_interferer/ber_singletone_css_slow-rate-False_-16.0_to_15.8MHz_2014-12-08_17-16-06.npy")
    f_oqpsk = np.arange(-fs_oqpsk/2, fs_oqpsk/2, 1e5)
    f_css = np.arange(-fs_css/2, fs_css/2, 2e5)

    plt.rcParams.update({'font.size': 14})
    plt.rcParams.update({'axes.labelsize': 'large'})
    plt.rcParams.update({'axes.labelsize': 'large'})

    plt.semilogy(f_css/1e6, css_slow, label='CSS 250 kb/s', marker='o')
    plt.semilogy(f_css/1e6, css_fast, label='CSS 1 Mb/s', marker='v')
    plt.semilogy(f_oqpsk/1e6, oqpsk, label='OQPSK', marker='s')
    plt.xlabel('Frequency [MHz]')
    plt.ylabel('BER')
    plt.grid()
    plt.legend(loc='lower center')
    plt.xlim([-10, 10])
    plt.ylim([1e-4, 1])
    plt.savefig('ber_singletone_sweep_combined.pdf', bbox='tight')
    plt.show()