%% IEEE 802.15.4 CSS PHY 250 kbps modulator

%% CSS PPDU format: [preamble, SFD, PHR, PSDU]
preamble = ones(1,80);
SFD = [-1 1 1 1 1 -1 1 -1 -1 -1 1 -1 -1 -1 1 1];
PHR = zeros(1,12); % bits [0..6] indicate length of payload in octets (bytes)
n_bytes_payload_dec = 3;
n_bits_payload_dec = n_bytes_payload_dec*8;
n_bytes_payload_bin = de2bi(n_bytes_payload_dec, 7);
PHR(1:7) = n_bytes_payload_bin; % number of payload bytes TODO: LSB or MSB first?

PSDU = randi(2,1,n_bits_payload_dec)-1;

% PHR and PSDU are bits (0/1) whereas preamble and SFD are NRZ (1/-1) coded
% and follow different signal paths in the modulator
data_bin = [PHR PSDU];
data_nrz = [preamble SFD];

%% divide binary and nrz coded data into I and Q stream
data_bin_I = data_bin(1:2:end);
data_bin_Q = data_bin(2:2:end);
data_nrz_I = data_nrz(1:2:end);
data_nrz_Q = data_nrz(2:2:end);

%% symbol mapping (6 bits equal one 32-chip codeword in 250 kbps mode)
sym_I = css_bit_to_symbols(data_bin_I);
sym_Q = css_bit_to_symbols(data_bin_Q);

%% interleaver (only in 250 kbps mode)
sym_I = css_bit_interleaver(sym_I);
sym_Q = css_bit_interleaver(sym_Q);

%% serialize I and Q streams
sym_I = reshape(sym_I', 1, []);
sym_Q = reshape(sym_Q', 1, []);

%% DQPSK modulation
sym_dqpsk = css_dqpsk_mod(sym_I, sym_Q);


