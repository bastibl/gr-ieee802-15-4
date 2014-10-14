#! /usr/bin python

import css_mod
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
	print "Generate IEEE 802.15.4 compliant CSS baseband signal"
	m = css_mod.modulator(slow_rate=True, phy_packetsize_bytes=18, nframes=20, chirp_number=1)
	[payload,baseband] = m.modulate_random()

	print len(baseband)
	s = np.fft.fft(baseband)
	plt.plot(abs(s))
	plt.show()

	with open('css_bb.bin', 'wb') as f:
		f.write(bytes(baseband[:]))




