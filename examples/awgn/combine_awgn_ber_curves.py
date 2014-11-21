#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
	oqpsk = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/oqpsk.npy")
	css_fast1 = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/cssfast1.npy")
	css_fast2 = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/cssfast2.npy")
	css_fast = np.concatenate((css_fast1, css_fast2))
	css_slow1 = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/cssslow1.npy")
	css_slow2 = np.load("/home/felixwunsch/src/gr-ieee802-15-4/examples/cssslow2.npy")
	css_slow = np.concatenate((css_slow1, css_slow2))
	css_slow_hd = css_slow[:,0]
	css_slow_sd = css_slow[:,1]
	css_fast_hd = css_fast[:,0]
	css_fast_sd = css_fast[:,1]	

	# SNR plot
	noiseampl_per_channel_db = np.arange(-10.0, 10, 0.5)
	noiseampl_per_channel = (10**(-noiseampl_per_channel_db/10))
	noisepower = 2.0/0.8166*(noiseampl_per_channel**2)
	signalpower_oqpsk = 1.0
	snr_oqpsk = 10*np.log10(signalpower_oqpsk/noisepower)
	signalpower_css = 1.0
	snr_css = 10*np.log10(signalpower_css/noisepower)
	plt.plot(snr_css, css_slow_hd, label="CSS hard decision (HD) high spreading factor (SF)")
	plt.plot(snr_css, css_slow_sd, label="CSS soft decision (SD) high SF")
	plt.plot(snr_css, css_fast_hd, label="CSS HD low SF")
	plt.plot(snr_css, css_fast_sd, label="CSS SD low SF")
	plt.plot(snr_oqpsk, oqpsk, label="OQPSK")
	plt.legend(loc='lower left')
	plt.yscale('log')
	plt.xlim([-22,2])
	plt.ylim([0.00001, 1])
	plt.ylabel("BER")
	plt.xlabel("SNR")
	plt.title("Comparison of IEEE 802.15.4 CSS/OQPSK PHY Layer in AWGN Channel")
	plt.grid()
	plt.show()

	# Eb/N0 plot
	css_Eb_noSF = 19.5998/0.8166 # sum(|norm_fac*chirp_seq|^2)/8 --> Energy per code bit
	css_Eb_hiSF = css_Eb_noSF*32.0/6
	css_Eb_loSF = css_Eb_noSF*4.0/3
	N0 = noisepower# int_0_T(n(t))dt/T ... using an amplitude of 10 in GRC results in a variance of 200 because 200 = 2*(10^2) (I&Q channel are added); This is possible because the mean power of the signal is 1
	# this Eb/N0 does not consider energy spent on headers, only the payload including the respective coding rate is considered because otherwise the number of payload bytes per frame would gain influence
	css_EbN0_noSF = 10*np.log10(css_Eb_noSF/N0) 
	css_EbN0_loSF = 10*np.log10(css_Eb_loSF/N0)
	css_EbN0_hiSF = 10*np.log10(css_Eb_hiSF/N0)
	# OQPSK
	oqpsk_Eb = 64.0/4 # the OQPSK signal has always magnitude 1; one codeword is 64 samples long and encodes 4 payload bits (in the 2450 MHz band)
	oqpsk_EbN0 = 10*np.log10(oqpsk_Eb/N0)
	# also plot uncoded BPSK for comparison (from MATLAB bertool)
	bpsk_EbN0 = np.arange(-5.0,21.0,1.0)
	bpsk_ber = np.array([0.213228018357620, 0.186113817483389, 0.158368318809598, 0.130644488522829, 0.103759095953406, 0.0786496035251426, 0.0562819519765415, 0.0375061283589260, 0.0228784075610853, 0.0125008180407376, 0.00595386714777866, 0.00238829078093281, 0.000772674815378444, 0.000190907774075993, 3.36272284196176e-05, 3.87210821552205e-06, 2.61306795357521e-07, 9.00601035062878e-09, 1.33293101753005e-10, 6.81018912878076e-13, 9.12395736262818e-16, 2.26739584445444e-19, 6.75896977065478e-24, 1.39601431090675e-29, 1.00107397357086e-36, 1.04424379188127e-45])
	plt.plot(css_EbN0_hiSF, css_slow_hd, label="CSS hard decision (HD) high spreading factor (SF)")
	plt.plot(css_EbN0_hiSF, css_slow_sd, label="CSS soft decision (SD) high SF")
	plt.plot(css_EbN0_loSF, css_fast_hd, label="CSS HD low SF")
	plt.plot(css_EbN0_loSF, css_fast_sd, label="CSS SD low SF")
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
	plt.show()


