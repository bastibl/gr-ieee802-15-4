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
#include "wireshark_connector_impl.h"
#include <gnuradio/ieee802_15_4/wireshark_connector.h>
#include <gr_io_signature.h>

#include <iostream>
#include <iomanip>

using namespace gr::ieee802_15_4;


class wireshark_connector_impl : public wireshark_connector {
public:

#define dout d_debug && std::cout

wireshark_connector_impl(bool debug) :
	gr_block ("wireshark_connector",
			gr_make_io_signature (0, 0, 0),
			gr_make_io_signature (1, 1, sizeof(uint8_t))),
			d_msg_offset(0),
			d_debug(debug) {

	message_port_register_in(pmt::mp("in"));

	pcap_global *hdr   = (pcap_global*)d_msg;
	hdr->magic_number  = 0xa1b2c3d4;
	hdr->version_major = 2;
	hdr->version_minor = 4;
	hdr->thiszone      = 0;
	hdr->sigfigs       = 0;
	hdr->snaplen       = 65535;
	hdr->network       = ZIGBEE;
	d_msg_len = sizeof(pcap_global);
}

~wireshark_connector_impl(void) {
}

void copy_message(const char *buf, int len) {

	pcap_pkt hdr;
	hdr.ts_sec   = 0;
	hdr.ts_usec  = 0;
	hdr.incl_len = len;
	hdr.orig_len = len;

	memcpy(d_msg, &hdr, sizeof(pcap_pkt));
	memcpy(d_msg + sizeof(pcap_pkt), buf, len);
	d_msg_len = sizeof(pcap_pkt) + len;
}

int general_work(int noutput, gr_vector_int& ninput_items,
                gr_vector_const_void_star& input_items,
		gr_vector_void_star& output_items ) {

	gr_complex *out = (gr_complex*)output_items[0];

	while(!d_msg_len) {
		pmt::pmt_t msg(delete_head_blocking(pmt::pmt_intern("in")));

		if(pmt::pmt_is_eof_object(msg)) {
			dout << "WIRESHARK: exiting" << std::endl;
			return -1;
		} else if(pmt::pmt_is_blob(msg)) {
			dout << "WIRESHARK: received new message" << std::endl;
			dout << "message length " << pmt::pmt_blob_length(msg) << std::endl;

			copy_message((const char*)pmt_blob_data(msg), pmt::pmt_blob_length(msg));
			break;
		} else if(pmt::pmt_is_pair(msg)) {
			pmt::pmt_t blob = pmt::pmt_cdr(msg);
			dout << "WIRESHARK: received new message" << std::endl;
			dout << "message length " << pmt::pmt_blob_length(blob) << std::endl;
			copy_message((const char*)pmt_blob_data(blob), pmt::pmt_blob_length(blob));
			break;
		}
	}

	int to_copy = std::min((d_msg_len - d_msg_offset), noutput);
	memcpy(out, d_msg + d_msg_offset, to_copy);

	dout << "WIRESHARK: d_msg_offset: " <<  d_msg_offset <<
		"   to_copy: " << to_copy << 
		"   d_msg_len " << d_msg_len << std::endl;

	d_msg_offset += to_copy;

	if(d_msg_offset == d_msg_len) {
		d_msg_offset = 0;
		d_msg_len = 0;
	}

	dout << "WIRESHARK: output size: " <<  noutput <<
		"   produced items: " << to_copy << std::endl;
	return to_copy;
}

private:
	bool        d_debug;
	int         d_msg_offset;
	int         d_msg_len;
	char        d_msg[256];
};

wireshark_connector::sptr
wireshark_connector::make(bool debug) {
	return gnuradio::get_initial_sptr(new wireshark_connector_impl(debug));
}
