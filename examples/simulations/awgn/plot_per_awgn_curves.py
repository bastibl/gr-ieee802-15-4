import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    plt.rcParams.update({'font.size': 10})
    plt.rcParams.update({'axes.labelsize': 'medium'})

    # OQPSK
    per_oqpsk_short = np.load("results/per_awgn_oqpsk_packetlen-12bytes_-20.0_to_-5.5dB_2014-12-17_10-05-08.npy")
    per_oqpsk_long = np.load("results/per_awgn_oqpsk_packetlen-127bytes_-20.0_to_-5.5dB_2014-12-17_09-57-05.npy")
    snr_oqpsk = np.arange(-20.0, -5.0, 0.5)
    oqpsk_bandwidth = 4e6
    oqpsk_datarate = 250e3
    ebn0_oqpsk = snr_oqpsk + 10*np.log10(oqpsk_bandwidth/oqpsk_datarate)

    # CSS 1 Mbps
    per_css_fast_short = np.load("results/per_awgn_css_slow_rate-False_packetlen-12bytes_-25.0_to_-5.5dB_2014-12-17_13-26-54.npy")
    per_css_fast_long = np.load("results/per_awgn_css_slow_rate-False_packetlen-127bytes_-25.0_to_-5.5dB_2014-12-17_13-33-40.npy")
    snr_css = np.arange(-25.0, -5.0, 0.5)
    css_bandwidth = 32e6
    css_fast_datarate = 1e6
    ebn0_css_fast = snr_css + 10*np.log10(css_bandwidth/css_fast_datarate)

    # CSS 250 kbps
    per_css_slow_short = np.load("results/per_awgn_css_slow_rate-True_packetlen-12bytes_-25.0_to_-5.5dB_2014-12-17_14-24-12.npy")
    per_css_slow_long = np.load("results/per_awgn_css_slow_rate-True_packetlen-127bytes_-25.0_to_-5.5dB_2014-12-17_11-35-23.npy")
    snr_css_slow = np.arange(-25.0, -5.0, 0.5)
    css_slow_datarate = 250e3
    ebn0_css_slow = snr_css + 10*np.log10(css_bandwidth/css_slow_datarate)

    # plot Eb/N0
    plt.figure(1)
    plt.semilogy(ebn0_css_slow, per_css_slow_short, label="CSS 250 kb/s: 1 byte payload", marker='o', color='b')
    plt.semilogy(ebn0_css_slow, per_css_slow_long, label="CSS 250 kb/s: 116 byte payload", marker='o', color='b', linestyle='--')
    plt.semilogy(ebn0_css_fast, per_css_fast_short, label="CSS 1 Mb/s: 1 byte payload", marker='v', color='g')
    plt.semilogy(ebn0_css_fast, per_css_fast_long, label="CSS 1 MB/s: 116 byte payload", marker='v', color='g', linestyle='--')
    plt.semilogy(ebn0_oqpsk, per_oqpsk_short, label="OQPSK: 1 byte payload", marker='s', color='r')
    plt.semilogy(ebn0_oqpsk, per_oqpsk_long, label="OQPSK: 116 byte payload", marker='s', color='r', linestyle='--')
    plt.legend(loc='lower left')
    plt.grid()
    plt.xlabel("Eb/N0")
    plt.ylabel("PER")
    plt.xlim([-5,10])
    plt.ylim([8e-4, 2])
    plt.savefig("per_ebn0_awgn.pdf")
    plt.show()

    # plot SNR
    plt.figure(2)
    plt.semilogy(snr_css, per_css_slow_short, label="CSS 250 kb/s: 1 byte payload", marker='o', color='b')
    plt.semilogy(snr_css, per_css_slow_long, label="CSS 250 kb/s: 116 byte payload", marker='o', color='b', linestyle='--')
    plt.semilogy(snr_css, per_css_fast_short, label="CSS 1 Mb/s: 1 byte payload", marker='v', color='g')
    plt.semilogy(snr_css, per_css_fast_long, label="CSS 1 MB/s: 116 byte payload", marker='v', color='g', linestyle='--')
    plt.semilogy(snr_oqpsk, per_oqpsk_short, label="OQPSK: 1 byte payload", marker='s', color='r')
    plt.semilogy(snr_oqpsk, per_oqpsk_long, label="OQPSK: 116 byte payload", marker='s', color='r', linestyle='--')
    # plt.legend(loc='lower left')
    plt.grid()
    plt.xlabel("SNR")
    plt.ylabel("PER")
    plt.xlim([-20,-5])
    plt.ylim([8e-4, 2])
    plt.savefig("per_snr_awgn.pdf")

    plt.show()

