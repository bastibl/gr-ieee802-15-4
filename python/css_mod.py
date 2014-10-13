import css_constants
import numpy as np

class modulator:
	def __init__(self, slow_rate=False, phy_packetsize_bytes=18, nframes=1):
		self.slow_rate = True
		self.phy_packetsize_bytes = phy_packetsize_bytes if phy_packetsize_bytes <= css_constants.max_phy_packetsize_bytes else css_constants.max_phy_packetsize_bytes
		if self.phy_packetsize_bytes % 6 != 0: # in order to match all periodicites the standard imposes the number of payload bytes has to be a multiple of 6
			self.phy_packetsize_bytes = self.phy_packetsize_bytes - (self.phy_packetsize_bytes % 6)
			print "changed packet size to", self.phy_packetsize_bytes
		self.nframes = nframes
		self.bits_per_symbol = 6 if self.slow_rate == True else 3
		self.codewords = css_constants.codewords_250kbps if self.slow_rate == True else css_constants.codewords_1mbps
		self.intlv_seq = css_constants.intlv_seq if self.slow_rate == True else []
		self.preamble = css_constants.preamble_250kbps if self.slow_rate == True else css_constants.preamble_1mbps
		self.SFD = css_constants.SFD_250kbps if self.slow_rate == True else css_constants.SFD_1mbps
		self.PHR = np.zeros((12,))

	def modulate_random(self):
		payload_total = np.zeros((0,));
		for n in range(self.nframes):
			print "process frame", n+1, "/", self.nframes
			print "- create random payload data"			
			payload = np.random.randint(0,2,size=(self.nframes*self.phy_packetsize_bytes*8,))
			payload_total = np.concatenate((payload_total, payload))

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

		complex_baseband = 0
		return [payload, complex_baseband]

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

	def create_PHR(self):
		payl_len_bitstring = '{0:07b}'.format(self.phy_packetsize_bytes)
		payl_len_list = [int(payl_len_bitstring[i],2) for i in range(0,len(payl_len_bitstring))]
		return payl_len_list[:]

	def create_frame(self, PPSDU):
		self.PHR[0:7] = self.create_PHR()
		return np.concatenate((self.preamble, self.SFD, self.PHR, PPSDU))

	def mod_QPSK(self, in_I, in_Q):
		print "QPSK not implemented yet"









