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

list(APPEND include_sources
	api.h
	mac.h
	mac_framer.h
	mac_deframer.h
	packet_sink.h
	qpsk_modulator.h
	rime_deframer.h
	rime_framer.h
	symbols_to_chips.h
)

install(
	FILES ${include_sources}
	DESTINATION ${GR_INCLUDE_DIR}/gnuradio/ieee802_15_4
	COMPONENT "ieee802_15_4_devel"
)
