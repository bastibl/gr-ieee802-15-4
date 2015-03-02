#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    oqpsk = np.load("results/ber_awgn_oqpsk_-30.0_to_-1.0dB_2014-12-04_13-31-41.npy")
    css_fast = np.load("results/ber_awgn_css_slow_rate-False_-30.0_to_-6.0dB_2014-12-04_13-42-42.npy")
    css_slow = np.load("results/ber_awgn_css_slow_rate-True_-30.0_to_-11.0dB_2014-12-04_14-13-13.npy")
    print "NOTE: This script applies a correction factor of +3dB to the SNR because there was a mistake in the simulation. The mistake is now fixed."
    snr_correction = 10*np.log10(2)
    snr_oqpsk = np.arange(-30.0, 0.0, 1.0) + snr_correction
    snr_css_fast = np.arange(-30.0, -5.0, 1.0) + snr_correction
    snr_css_slow = np.arange(-30.0, -10.0, 1.0) + snr_correction

    plt.rcParams.update({'font.size': 14})
    plt.rcParams.update({'axes.labelsize': 'large'})

    # # SNR plot
    plt.plot(snr_css_slow, css_slow, label="CSS 250 kb/s", marker='o')
    plt.plot(snr_css_fast, css_fast, label="CSS 1 Mb/s", marker='v')
    plt.plot(snr_oqpsk, oqpsk, label="OQPSK", marker='s')
    plt.legend(loc='lower left')
    plt.yscale('log')
    plt.xlim([-27,0])
    plt.ylim([0.00002, 1])
    plt.ylabel("BER")
    plt.xlabel("SNR [dB]")
    plt.grid()
    plt.savefig("ber_snr_awgn_oqpsk_css.pdf", bbox_inches='tight')
    plt.show()

    # Eb/N0 plot
    # this Eb/N0 does not consider energy spent on headers, only the payload including the respective coding rate is considered because otherwise the number of payload bytes per frame would gain influence
    css_EbN0_loSF = snr_css_fast + 10 * np.log10(32e6 / 1e6)
    css_EbN0_hiSF = snr_css_slow + 10 * np.log10(32e6 / 250e3)
    # OQPSK
    oqpsk_EbN0 = snr_oqpsk + 10 * np.log10(4e6 / 250e3)
    # also plot uncoded BPSK for comparison (from MATLAB bertool)
    bpsk_EbN0 = np.arange(-5.0, 21.0, 1.0)
    bpsk_ber = np.array([0.213228018357620, 0.186113817483389, 0.158368318809598, 0.130644488522829, 0.103759095953406,
                         0.0786496035251426, 0.0562819519765415, 0.0375061283589260, 0.0228784075610853,
                         0.0125008180407376, 0.00595386714777866, 0.00238829078093281, 0.000772674815378444,
                         0.000190907774075993, 3.36272284196176e-05, 3.87210821552205e-06, 2.61306795357521e-07,
                         9.00601035062878e-09, 1.33293101753005e-10, 6.81018912878076e-13, 9.12395736262818e-16,
                         2.26739584445444e-19, 6.75896977065478e-24, 1.39601431090675e-29, 1.00107397357086e-36,
                         1.04424379188127e-45])
    plt.plot(css_EbN0_hiSF, css_slow, label="CSS 250 kb/s", marker='o')
    plt.plot(css_EbN0_loSF, css_fast, label="CSS 1 Mb/s", marker='v')
    plt.plot(oqpsk_EbN0, oqpsk, label="OQPSK", marker='s')
    # plt.plot(bpsk_EbN0, bpsk_ber, label="uncoded BPSK \n(theoretical)", marker='x')
    plt.legend(loc='lower left')
    plt.yscale('log')
    plt.xlim([-5, 13])
    plt.ylim([0.00005, 1])
    plt.ylabel("BER")
    plt.xlabel("Eb/N0 [dB]")
    plt.grid()
    plt.savefig("ber_ebn0_awgn_oqpsk_css.pdf", bbox_inches='tight')
    plt.show()


