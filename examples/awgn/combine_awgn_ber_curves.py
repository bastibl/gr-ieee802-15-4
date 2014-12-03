#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
	oqpsk = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/awgn/ber_awgn_oqpsk_-30.0_to_-6.0dB_2014-11-28_14-34-27.npy")
	css_fast = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/awgn/ber_awgn_css_slow_rate-False_-30.0_to_-6.0dB_2014-11-28_14-25-09.npy")
	css_slow = np.load("/home/wunsch/src/gr-ieee802-15-4/examples/awgn/tmp_ber_awgn_css_slow_rate-True_-30.0_to_-11.0dB.npy")
	snr_oqpsk = np.arange(-25.0, 0.0, 1.0)
	snr_css_fast = np.arange(-30.0, -5.0, 1.0)
	snr_css_slow = np.arange(-30.0, -10.0, 1.0)

	# # SNR plot
	plt.plot(snr_css_slow, css_slow, label="CSS soft decision (SD) 250 kbps")
	plt.plot(snr_css_fast, css_fast, label="CSS SD 1 Mbps")
	plt.plot(snr_oqpsk, oqpsk, label="OQPSK 250 kbps")
	plt.legend(loc='lower left')
	plt.yscale('log')
	# plt.xlim([-22,2])
	plt.ylim([0.00001, 1])
	plt.ylabel("BER")
	plt.xlabel("SNR")
	plt.title("Comparison of IEEE 802.15.4 CSS/OQPSK PHY Layer in AWGN Channel")
	plt.grid()
	plt.savefig("ber_snr_awgn_oqpsk_css.pdf")
	plt.show()

	# Eb/N0 plot
	css_Eb_noSF = 19.0007 # sum(|norm_fac*chirp_seq|^2)/8 --> Energy per code bit
	css_Eb_hiSF = css_Eb_noSF*32.0/6
	css_Eb_loSF = css_Eb_noSF*4.0/3
	# this Eb/N0 does not consider energy spent on headers, only the payload including the respective coding rate is considered because otherwise the number of payload bytes per frame would gain influence
	css_EbN0_loSF = 10*np.log10(css_Eb_loSF) + snr_css_fast
	css_EbN0_hiSF = 10*np.log10(css_Eb_hiSF) + snr_css_slow
	# OQPSK
	oqpsk_Eb = 64.0/4 # the OQPSK signal has always magnitude 1; one codeword is 64 samples long and encodes 4 payload bits (in the 2450 MHz band)
	oqpsk_EbN0 = 10*np.log10(oqpsk_Eb) + snr_oqpsk
	# also plot uncoded BPSK for comparison (from MATLAB bertool)
	bpsk_EbN0 = np.arange(-5.0,21.0,1.0)
	bpsk_ber = np.array([0.213228018357620, 0.186113817483389, 0.158368318809598, 0.130644488522829, 0.103759095953406, 0.0786496035251426, 0.0562819519765415, 0.0375061283589260, 0.0228784075610853, 0.0125008180407376, 0.00595386714777866, 0.00238829078093281, 0.000772674815378444, 0.000190907774075993, 3.36272284196176e-05, 3.87210821552205e-06, 2.61306795357521e-07, 9.00601035062878e-09, 1.33293101753005e-10, 6.81018912878076e-13, 9.12395736262818e-16, 2.26739584445444e-19, 6.75896977065478e-24, 1.39601431090675e-29, 1.00107397357086e-36, 1.04424379188127e-45])
	plt.plot(css_EbN0_hiSF, css_slow, label="CSS soft decision (SD) 250 kbps")
	plt.plot(css_EbN0_loSF, css_fast, label="CSS SD 1 Mbps")
	plt.plot(oqpsk_EbN0, oqpsk, label="OQPSK")
	plt.plot(bpsk_EbN0, bpsk_ber, label="uncoded BPSK (theoretical)")
	plt.legend(loc='lower left')
	plt.yscale('log')
	plt.xlim([-2,15])
	plt.ylim([0.00001, 1])
	plt.ylabel("BER")
	plt.xlabel("Eb/N0")
	plt.title("Comparison of IEEE 802.15.4 CSS and OQPSK PHY Layer in AWGN Channel")
	plt.grid()
	plt.savefig("ber_ebn0_awgn_oqpsk_css.pdf")
	plt.show()


