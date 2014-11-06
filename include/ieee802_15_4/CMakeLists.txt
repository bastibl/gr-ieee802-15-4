#
# Copyright 2013 Free Software Foundation, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
install(FILES
	access_code_prefixer.h
	api.h
	mac.h
	packet_sink.h
	rime_stack.h
	fragmentation.h
    phr_prefixer.h
    zeropadding_b.h
    codeword_mapper_bi.h
    interleaver_ii.h
    qpsk_mapper_if.h
    dqpsk_mapper_ff.h
    dqcsk_mapper_fc.h
    preamble_sfd_prefixer_ii.h
    dqcsk_demapper_cf.h
    qpsk_demapper_fi.h
    codeword_demapper_ib.h
    zeropadding_removal_b.h
    phr_removal.h
    make_pair_with_blob.h
    matched_filter_ff.h
    chips_to_bits_fb.h DESTINATION ${GR_INCLUDE_DIR}/gnuradio/ieee802_15_4
	COMPONENT "ieee802_15_4_devel"
)
