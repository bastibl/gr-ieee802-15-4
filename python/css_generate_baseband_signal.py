#! /usr/bin python

import css_mod
import css_constants
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

if __name__ == "__main__":
	print "Generate IEEE 802.15.4 compliant CSS baseband signal"
	m = css_mod.modulator(slow_rate=True, phy_packetsize_bytes=18, nframes=100, chirp_number=4)
	[payload,baseband] = m.modulate_random()
	

	# plot PSD and frequency mask
	s = abs(np.fft.fftshift(np.fft.fft(baseband)))**2
	freq = np.linspace(-css_constants.bb_samp_rate/2, css_constants.bb_samp_rate/2-1/css_constants.bb_samp_rate, len(s))
	mask = np.zeros(len(s))
	for i in range(len(mask)):
		if abs(freq[i]) > 22e6:
			mask[i] = 1e-5
		if abs(freq[i]) > 11e6:
			mask[i] = 1e-3
		if abs(freq[i]) <= 11e6:
			mask[i] = 1
	f, axarr = plt.subplots(3,1)
	s_norm = s/max(s)
	axarr[0].plot(freq, 10*np.log10(s_norm))
	axarr[0].plot(freq, 10*np.log10(mask), 'r')
	axarr[0].set_title("Complex baseband spectrum and frequency mask")
	axarr[0].set_ylabel("|S| [dB]")
	axarr[0].set_xlabel("Hz")
	axarr[0].set_ylim([-50,0])
	axarr[0].set_xlim([freq[0], freq[-1]])

	# plot time signal magnitude
	t = np.linspace(0,1,css_constants.bb_samp_rate+1)
	t = t[:1500]
	axarr[1].plot(t, abs(baseband[:len(t)]))
	axarr[1].set_title("Complex baseband magnitude")
	axarr[1].set_xlabel("s")
	axarr[1].set_ylabel("|s(t)|")

	# plot real part of time signal
	axarr[2].plot(t,baseband[:len(t)].real)
	axarr[2].set_title("Real part of time signal using chirp sequence #"+str(m.chirp_number))
	axarr[2].set_xlabel("s")
	axarr[2].set_ylabel("R{s(t)}")

	# plot auto-/crosscorrelation of chirp sequences
	ccf = []
	for i in range(4):
		for k in range(4):
			tmp = abs(np.correlate(m.possible_chirp_sequences[i], m.possible_chirp_sequences[k], mode='same'))
			ccf.append(tmp)

	f, axarr = plt.subplots(4,4)
	for i in range(4):
		for k in range(4):
			titlestring = "("+str(i+1)+","+str(k+1)+")"
			axarr[i,k].plot(ccf[i*4+k], label=titlestring)
			axarr[i,k].legend()
	f.suptitle("Cross correlation of chirp sequence pairs (no time gaps)")

	

	plt.show()




