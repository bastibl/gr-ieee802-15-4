#! /usr/bin python

import css_mod
import css_constants
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

if __name__ == "__main__":
	print "Generate IEEE 802.15.4 compliant CSS baseband signal"
	m = css_mod.modulator(slow_rate=True, phy_packetsize_bytes=18, nframes=1, chirp_number=1)
	[payload,baseband] = m.modulate_random()

	s = np.fft.fftshift(np.fft.fft(baseband))
	f = np.linspace(-css_constants.bb_samp_rate/2, css_constants.bb_samp_rate/2-1/css_constants.bb_samp_rate, len(s))

	plt.figure()
	plt.plot(f, 10*np.log10(abs(s)**2))
	plt.title('Complex baseband spectrum')
	plt.ylabel('|S|')
	plt.xlabel('Hz')

	t = np.linspace(0,1,css_constants.bb_samp_rate+1)
	t = t[:3000]
	plt.figure()
	plt.plot(t, abs(baseband[:len(t)]))
	plt.title('Complex baseband magnitude')
	plt.xlabel('s')
	plt.ylabel('|s(t)|')
	

	plt.show()




