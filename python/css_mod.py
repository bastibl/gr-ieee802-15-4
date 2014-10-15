import css_constants
import numpy as np
import matplotlib.pyplot as plt

class modulator:
	def __init__(self, slow_rate=False, phy_packetsize_bytes=18, nframes=1, chirp_number=1):
		self.slow_rate = True
		self.phy_packetsize_bytes = phy_packetsize_bytes if phy_packetsize_bytes <= css_constants.max_phy_packetsize_bytes else css_constants.max_phy_packetsize_bytes
		if self.phy_packetsize_bytes % 6 != 0: # in order to match all periodicites the standard imposes the number of payload bytes has to be a multiple of 6
			self.phy_packetsize_bytes = self.phy_packetsize_bytes - (self.phy_packetsize_bytes % 6)
			print "changed packet size to", self.phy_packetsize_bytes
		self.nframes = nframes
		self.chirp_number = chirp_number
		self.bits_per_symbol = 6 if self.slow_rate == True else 3
		self.codewords = css_constants.codewords_250kbps if self.slow_rate == True else css_constants.codewords_1mbps
		self.intlv_seq = css_constants.intlv_seq if self.slow_rate == True else []
		self.preamble = css_constants.preamble_250kbps if self.slow_rate == True else css_constants.preamble_1mbps
		self.SFD = css_constants.SFD_250kbps if self.slow_rate == True else css_constants.SFD_1mbpsg
		self.PHR = np.zeros((12,))
		self.PHR[0:7] = self.gen_PHR()
		self.rcfilt = self.gen_rcfilt()
		self.possible_chirp_sequences = self.gen_chirp_sequences()
		if self.chirp_number < 1 or self.chirp_number > 4:
			print "Invalid chirp sequence number, must be [1..4]. Use chirp 1"
			self.chirp_number = 1
		self.chirp_seq = self.possible_chirp_sequences[self.chirp_number-1]
		self.n_tau = css_constants.n_tau[self.chirp_number-1]

	def gen_rcfilt(self):
		alpha = 0.25
		rcfilt = np.ones((css_constants.n_sub,))
		start_slope = round((1-alpha)/(1+alpha)*css_constants.n_sub/2)
		rcfilt[len(rcfilt)/2+start_slope::] = [0.5*(1+np.cos((1+alpha)*np.pi/(alpha*css_constants.n_sub)*i)) for i in range(int(css_constants.n_sub/2-start_slope))]
		rcfilt[0:len(rcfilt)/2-start_slope] = rcfilt[-1:len(rcfilt)/2+start_slope-1:-1]
		return rcfilt

	def gen_chirp_sequences(self):
		# first, generate subchirps
		subchirp_low_up = np.array([np.exp(1j*(2*np.pi*css_constants.fc_low + css_constants.mu/2*i/css_constants.bb_samp_rate)*i/css_constants.bb_samp_rate)*self.rcfilt[i] for i in range(css_constants.n_sub)])
		subchirp_low_down = np.array([np.exp(1j*(2*np.pi*css_constants.fc_low - css_constants.mu/2*i/css_constants.bb_samp_rate)*i/css_constants.bb_samp_rate)*self.rcfilt[i] for i in range(css_constants.n_sub)])
		subchirp_high_up = np.array([np.exp(1j*(2*np.pi*css_constants.fc_high + css_constants.mu/2*i/css_constants.bb_samp_rate)*i/css_constants.bb_samp_rate)*self.rcfilt[i] for i in range(css_constants.n_sub)])
		subchirp_high_down = np.array([np.exp(1j*(2*np.pi*css_constants.fc_high - css_constants.mu/2*i/css_constants.bb_samp_rate)*i/css_constants.bb_samp_rate)*self.rcfilt[i] for i in range(css_constants.n_sub)])

		# put together the chirp sequences (without DQPSK symbols)
		chirp_seq_I = np.concatenate((subchirp_low_up, subchirp_high_up, subchirp_high_down, subchirp_low_down))
		chirp_seq_II = np.concatenate((subchirp_high_up, subchirp_low_down, subchirp_low_up, subchirp_high_down))
		chirp_seq_III = np.concatenate((subchirp_low_down, subchirp_high_down, subchirp_high_up, subchirp_low_up))
		chirp_seq_IV = np.concatenate((subchirp_high_down, subchirp_low_up, subchirp_low_down, subchirp_high_up))

		return [chirp_seq_I, chirp_seq_II, chirp_seq_III, chirp_seq_IV]

	def gen_PHR(self):
		payl_len_bitstring = '{0:07b}'.format(self.phy_packetsize_bytes)
		payl_len_list = [int(payl_len_bitstring[i],2) for i in range(0,len(payl_len_bitstring))]
		return payl_len_list

	def modulate_random(self):
		payload_total = np.zeros((0,));
		complex_baseband_total = np.zeros((0,))

		for n in range(self.nframes):
			print "process frame", n+1, "/", self.nframes
			print "- create random payload data and PHR"	

			payload = np.random.randint(0,2,size=(self.nframes*self.phy_packetsize_bytes*8,))
			payload_total = np.concatenate((payload_total, payload))
			payload = np.concatenate((self.PHR, payload)) # append payload to PHR

			print "- divide payload up into I and Q stream"
			[payload_I, payload_Q] = self.demux(payload)

			print "- map bits to codewords"
			payl_sym_I = self.bits_to_codewords(payload_I)
			payl_sym_Q = self.bits_to_codewords(payload_Q)
		
			if self.slow_rate == True:
				print "- interleave codewords if in 250 kbps mode"
				payl_sym_I = self.interleaver(payl_sym_I)
				payl_sym_Q = self.interleaver(payl_sym_Q)

			print "- create frame structure"
			frame_sym_I = self.create_frame(payl_sym_I)
			frame_sym_Q = self.create_frame(payl_sym_Q)

			print "- modulate DQPSK symbols"
			frame_QPSK = self.mod_QPSK(frame_sym_I, frame_sym_Q)
			frame_DQPSK = self.mod_DQPSK(frame_QPSK)

			print "- modulate DQCSK symbols"
			frame_DQCSK = self.mod_DQCSK(frame_DQPSK)
			complex_baseband_total = np.concatenate((complex_baseband_total,frame_DQCSK)) 	


		return [payload_total, complex_baseband_total]

	def modulate(payload):
		print "not implemented yet, shall be used to pipe in special payload"


	def demux(self, in_stream):
		return [in_stream[0::2], in_stream[1::2]]

	def bits_to_codewords(self, in_bits):
		in_bits = in_bits.reshape((len(in_bits)/self.bits_per_symbol), self.bits_per_symbol)
		idx = in_bits.dot(1 << np.arange(in_bits.shape[-1] - 1, -1, -1))
		len_cw = len(self.codewords[0])
		cw_serialized = np.array([self.codewords[int(i)] for i in idx])
		cw_serialized = cw_serialized.reshape((len(cw_serialized.flat),))
		return cw_serialized

	def interleaver(self, in_stream):
		return np.array([in_stream[i] for i in self.intlv_seq])

	def create_frame(self, PHR_PPSDU):
		return np.concatenate((self.preamble, self.SFD, PHR_PPSDU))

	def mod_QPSK(self, in_I, in_Q):
		sym_out = []
		QPSK_symbols = [1+0j, 0+1j, 0-1j, -1+0j]
		for i in range(len(in_I)):
			if (in_I[i], in_Q[i]) == (1,1):	
				sym_out.append(QPSK_symbols[0])
			elif (in_I[i], in_Q[i]) == (-1,1):
				sym_out.append(QPSK_symbols[1])
			elif (in_I[i], in_Q[i]) == (1,-1):
				sym_out.append(QPSK_symbols[2])
			elif (in_I[i], in_Q[i]) == (-1,-1):
				sym_out.append(QPSK_symbols[3])
			else:
				print "ERROR in mod_QPSK: Invalid input sequence"
		return sym_out

	def mod_DQPSK(self, in_QPSK):
		# a distance of 4 symbols is used to calculate the phase difference
		# the delay chain is initialized with exp(1j*pi/4)
		delay_chain = np.array([np.exp(1j*np.pi/4) for i in range(4)])
		sym_out = []
		for i in range(len(in_QPSK)):
			sym_out.append(in_QPSK[i]*delay_chain[3])
			delay_chain[1::] = delay_chain[0::-1]
			delay_chain[0] = sym_out[i]
		return sym_out

	def mod_DQCSK(self, in_DQPSK):
		if len(in_DQPSK) % 4 != 0:
			print "Number of DQCSK input symbols must be a multiple of 4. Drop tailing symbols"
			in_DQPSK = in_DQPSK[:-len(in_DQPSK)%4]
		
		n_seq = len(in_DQPSK)/4
		cplx_bb = np.zeros((0,), dtype=np.complex64)
		
		time_gap_1 = np.zeros((css_constants.n_chirp - 2*self.n_tau - 4*css_constants.n_sub,),dtype=np.complex64)
		time_gap_2 = np.zeros((css_constants.n_chirp + 2*self.n_tau - 4*css_constants.n_sub,),dtype=np.complex64)
		print "len gap1:", len(time_gap_1), "len gap2:", len(time_gap_2)
		for i in range(n_seq):
			tmp = self.chirp_seq
			for k in range(4):
				tmp[k*css_constants.n_sub:(k+1)*css_constants.n_sub] *= in_DQPSK[i*4+k]
			cplx_bb = np.concatenate((cplx_bb, tmp))
			if i%2 == 0:
				cplx_bb = np.concatenate((cplx_bb, time_gap_1))
			else:
				cplx_bb = np.concatenate((cplx_bb, time_gap_2))
		return cplx_bb








