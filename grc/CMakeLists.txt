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
    ieee802_15_4_access_code_prefixer.xml
    ieee802_15_4_mac.xml
    ieee802_15_4_packet_sink.xml
    ieee802_15_4_rime_stack.xml
    ieee802_15_4_phr_prefixer.xml
    ieee802_15_4_zeropadding_b.xml
    ieee802_15_4_codeword_mapper_bi.xml
    ieee802_15_4_interleaver_ii.xml
    ieee802_15_4_qpsk_mapper_if.xml
    ieee802_15_4_dqpsk_mapper_ff.xml
    ieee802_15_4_dqcsk_mapper_fc.xml
    ieee802_15_4_preamble_sfd_prefixer_ii.xml
    ieee802_15_4_dqcsk_demapper_cc.xml
    ieee802_15_4_qpsk_demapper_fi.xml
    ieee802_15_4_codeword_demapper_ib.xml
    ieee802_15_4_zeropadding_removal_b.xml
    ieee802_15_4_phr_removal.xml
    ieee802_15_4_chips_to_bits_fb.xml
    ieee802_15_4_access_code_removal_b.xml
    ieee802_15_4_dqpsk_soft_demapper_cc.xml
    ieee802_15_4_deinterleaver_ff.xml
    ieee802_15_4_codeword_soft_demapper_fb.xml
    ieee802_15_4_frame_buffer_cc.xml
    ieee802_15_4_multiuser_chirp_detector_cc.xml
    ieee802_15_4_preamble_tagger_cc.xml DESTINATION share/gnuradio/grc/blocks
)
