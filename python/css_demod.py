import css_constants
import css_phy
import numpy as np
import matplotlib.pyplot as plt

def c_corrcoef(a,b):
	# formula: sum(a*conj(b))/(sum(a*conj(a))*sum(b*conj(b)))
	num = sum(a*np.conj(b))
	bias = 1e-9 # this is needed in case either a or b are equal to 0
	denom = (sum(a*np.conj(a))+bias)*(sum(b*np.conj(b)) + bias)
	return num/denom

class demodulator(css_phy.physical_layer):
	def demodulate(self, iq_in):
		payload_total = []
		len_iq_in = len(iq_in)
		pos = 0
		chirp_seq_ctr = 0
		subchirp_ctr = 0
		subchirps = self.chirp_seq.reshape((4,css_constants.n_sub))
		corr_out = []
		n_sub = css_constants.n_sub
		while len_iq_in - pos >= n_sub:
			f, axarr = plt.subplots(2)
			axarr[0].plot(iq_in[pos:pos+n_sub].real, label='real')
			axarr[0].plot(iq_in[pos:pos+n_sub].imag, label='imag')
			axarr[0].plot(abs(iq_in[pos:pos+n_sub]), label='mag')
			axarr[0].legend()
			axarr[0].set_title("RX input")
			axarr[0].set_ylim([-1.1, 1.1])
			axarr[1].plot(subchirps[subchirp_ctr].real, label='real')
			axarr[1].plot(subchirps[subchirp_ctr].imag, label='imag')
			axarr[1].plot(abs(subchirps[subchirp_ctr]), label='mag')
			axarr[1].legend()
			axarr[1].set_title("Reference subchirp")
			axarr[1].set_ylim([-1.1, 1.1])
			f.suptitle("RX correlator")
			plt.show()

			tmp = c_corrcoef(iq_in[pos:pos+n_sub], subchirps[subchirp_ctr])
			pos += n_sub
			corr_out.append((abs(tmp), np.angle(tmp)))
			subchirp_ctr += 1
			if subchirp_ctr == self.n_subchirps:
				if chirp_seq_ctr == 0: 
					pos += len(self.time_gap_1)
				else:
					pos += len(self.time_gap_2)
				subchirp_ctr = 0
				chirp_seq_ctr = (chirp_seq_ctr + 1) % 2
		return corr_out



