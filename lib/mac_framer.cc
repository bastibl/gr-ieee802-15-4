/*
 * Copyright (C) 2013 Bastian Bloessl <bloessl@ccs-labs.org>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#include <gnuradio/ieee802_15_4/mac_framer.h>
#include <gnuradio/io_signature.h>

#include <iostream>
#include <iomanip>

using namespace gr::ieee802_15_4;


class mac_framer_impl : public mac_framer {
public:

#define dout d_debug && std::cout

mac_framer_impl(bool debug) :
	gr::block ("mac_framer",
			gr::io_signature::make (0, 0, 0),
			gr::io_signature::make (1, 1, sizeof(uint8_t))),
			d_msg_offset(0),
			d_seq_nr(0),
			d_debug(debug) {

	message_port_register_in(pmt::mp("in"));
}

~mac_framer_impl(void) {
}

uint16_t crc16(char *buf, int len) {
	uint16_t crc = 0;

	for(int i = 0; i < len; i++) {
		for(int k = 0; k < 8; k++) {
			int input_bit = (!!(buf[i] & (1 << k)) ^ (crc & 1));
			crc = crc >> 1;
			if(input_bit) {
				crc ^= (1 << 15);
				crc ^= (1 << 10);
				crc ^= (1 <<  3);
			}
		}
	}

	return crc;
}

void generate_mac(const char *buf, int len) {

	// start frame
	d_msg[0] = 0x00;
	d_msg[1] = 0x00;
	d_msg[2] = 0x00;
	d_msg[3] = 0x00;
	d_msg[4] = 0xA7;

	// length
	d_msg[5] = 3 + 6 + len + 2;

	// FCF
	d_msg[6] = 0x41;
	d_msg[7] = 0x88;

	// seq nr
	d_msg[8] = d_seq_nr++;

	// addr info
	d_msg[ 9] = 0xcd;
	d_msg[10] = 0xab;
	d_msg[11] = 0xff;
	d_msg[12] = 0xff;
	d_msg[13] = 0x40;
	d_msg[14] = 0xe8;

	std::memcpy(d_msg + 15, buf, len);

	uint16_t crc = crc16(d_msg + 6, len + 9);

	d_msg[15 + len] = crc & 0xFF;
	d_msg[16 + len] = crc >> 8;

	d_msg_len = 15 + len + 2;

	dout << std::dec << "msg len " << d_msg_len <<
	        "    len " << len << std::endl;
}

void print_message() {
	for(int i = 0; i < d_msg_len; i++) {
		dout << std::setfill('0') << std::setw(2) << std::hex << ((unsigned int)d_msg[i] & 0xFF) << std::dec << " ";
		if(i % 16 == 15) {
			dout << std::endl;
		}
	}
	dout << std::endl;
}

int general_work(int noutput, gr_vector_int& ninput_items,
                gr_vector_const_void_star& input_items,
		gr_vector_void_star& output_items ) {

	gr_complex *out = (gr_complex*)output_items[0];

	while(!d_msg_offset) {
		pmt::pmt_t msg(delete_head_blocking(pmt::intern("in")));

		if(pmt::is_eof_object(msg)) {
			dout << "MAC: exiting" << std::endl;
			return -1;
		}

		if(pmt::is_blob(msg)) {
			dout << "MAC: received new message" << std::endl;
			dout << "message length " << pmt::blob_length(msg) << std::endl;

			generate_mac((const char*)blob_data(msg), pmt::blob_length(msg));
			print_message();
			break;
		}
	}

	int to_copy = std::min((d_msg_len - d_msg_offset), noutput);
	memcpy(out, d_msg + d_msg_offset, to_copy);

	dout << "MAC: d_msg_offset: " <<  d_msg_offset <<
		"   to_copy: " << to_copy << 
		"   d_msg_len " << d_msg_len << std::endl;

	d_msg_offset += to_copy;

	if(d_msg_offset == d_msg_len) {
		d_msg_offset = 0;
	}

	dout << "MAC: output size: " <<  noutput <<
		"   produced items: " << to_copy << std::endl;
	return to_copy;
}

private:
	bool        d_debug;
	int         d_msg_offset;
	int         d_msg_len;
	uint8_t     d_seq_nr;
	char        d_msg[256];
};

mac_framer::sptr
mac_framer::make(bool debug) {
	return gnuradio::get_initial_sptr(new mac_framer_impl(debug));
}
