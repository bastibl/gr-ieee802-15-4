import css_constants
import css_phy
import numpy as np
import matplotlib.pyplot as plt

def c_corrcoef(a,b):
	# formula: sum(a*conj(b))/(sum(a*conj(a))*sum(b*conj(b)))
	num = sum(a*np.conj(b))
	denom = np.sqrt(sum(a*np.conj(a))*sum(b*np.conj(b)))
	if denom == 0:
		return 0
	return num/denom

class demodulator(css_phy.physical_layer):
	def demodulate(self, iq_in):
		self.demod_preamble(iq_in)
		sym_DQPSK = self.demod_DQCSK(iq_in)	
		return sym_DQPSK	

	def demod_preamble(self, sym_in):
		# preambles for 250kbps and 1mbps differ in their length
		if len(sym_in) < len(self.preamble)/2:
			raise Exception("Not enough input symbols")	


	def demod_DQCSK(self, iq_in):
		len_iq_in = len(iq_in)
		pos = 0
		chirp_seq_ctr = 0
		subchirp_ctr = 0
		subchirps = self.chirp_seq.reshape((4,css_constants.n_sub))
		corr_out = []
		n_sub = css_constants.n_sub
		while len_iq_in - pos >= n_sub:
			# f, axarr = plt.subplots(2)
			# axarr[0].plot(iq_in[pos:pos+n_sub].real, label='real')
			# axarr[0].plot(iq_in[pos:pos+n_sub].imag, label='imag')
			# axarr[0].plot(abs(iq_in[pos:pos+n_sub]), label='mag')
			# axarr[0].legend()
			# axarr[0].set_title("RX input")
			# axarr[0].set_ylim([-1.1, 1.1])
			# axarr[1].plot(subchirps[subchirp_ctr].real, label='real')
			# axarr[1].plot(subchirps[subchirp_ctr].imag, label='imag')
			# axarr[1].plot(abs(subchirps[subchirp_ctr]), label='mag')
			# axarr[1].legend()
			# axarr[1].set_title("Reference subchirp")
			# axarr[1].set_ylim([-1.1, 1.1])
			# f.suptitle("RX correlator")
			# plt.show()

			tmp = c_corrcoef(iq_in[pos:pos+n_sub], subchirps[subchirp_ctr])
			pos += n_sub
			corr_out.append(tmp)
			subchirp_ctr += 1
			if subchirp_ctr == self.n_subchirps:
				if chirp_seq_ctr == 0: 
					pos += len(self.time_gap_1)
				else:
					pos += len(self.time_gap_2)
				subchirp_ctr = 0
				chirp_seq_ctr = (chirp_seq_ctr + 1) % 2
		return np.array(corr_out)

	def demod_DQPSK(self, sym_in, delay_chain_state=np.array([np.exp(-1j*np.pi/4) for i in range(4)])):
		delay_chain = delay_chain_state
		sym_out = []
		for i in range(len(sym_in)):
			sym_out.append(sym_in[i]*delay_chain[3])
			delay_chain[1::] = delay_chain[0::-1]
			delay_chain[0] = sym_out[i]
		return sym_out

