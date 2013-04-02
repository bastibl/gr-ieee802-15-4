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
    ieee802_15_4_packet_sink.xml
    ieee802_15_4_qpsk_modulator.xml
    ieee802_15_4_symbols_to_chips.xml
    ieee802_15_4_rime_framer.xml
    ieee802_15_4_mac_framer.xml
    ieee802_15_4_mac.xml
    ieee802_15_4_rime_deframer.xml
    ieee802_15_4_mac_deframer.xml
    DESTINATION share/gnuradio/grc/blocks
)
