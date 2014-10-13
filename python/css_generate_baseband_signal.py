#! /usr/bin python

import css_mod

if __name__ == "__main__":
	print "Generate IEEE 802.15.4 compliant CSS baseband signal"
	m = css_mod.modulator(slow_rate=False, phy_packetsize_bytes=18, nframes=2)
	[payload,baseband] = m.modulate_random()


