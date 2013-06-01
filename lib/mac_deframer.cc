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
#include <gnuradio/ieee802_15_4/mac_deframer.h>

#include <gnuradio/io_signature.h>
#include <gnuradio/block_detail.h>
#include <string.h>

using namespace gr::ieee802_15_4;

class mac_deframer_impl : public mac_deframer {

public:

mac_deframer_impl() : gr::block("mac_deframer",
		gr::io_signature::make (0, 0, 0),
		gr::io_signature::make (0, 0, 0)) {

	message_port_register_out(pmt::mp("pdu out"));

	message_port_register_in(pmt::mp("pdu in"));
	set_msg_handler(pmt::mp("pdu in"), boost::bind(&mac_deframer_impl::make_frame, this, _1));
}

~mac_deframer_impl() {

}

void make_frame (pmt::pmt_t msg) {

	pmt::pmt_t blob;

	if(pmt::is_eof_object(msg)) {
		message_port_pub(pmt::mp("pdu out"), pmt::PMT_EOF);
		detail().get()->set_done(true);
		return;
	} else if(pmt::is_pair(msg)) {
		blob = pmt::cdr(msg);
	} else {
		assert(false);
	}

	size_t data_len = pmt::blob_length(blob);
	if(data_len < 13) {
		return;
	}

	// FIXME: here should be a crc check
	pmt::pmt_t mac_payload = pmt::make_blob((char*)pmt::blob_data(blob) + 9 , data_len - 9 - 2);

        message_port_pub(pmt::mp("pdu out"), pmt::cons(pmt::PMT_NIL, mac_payload));
}

};

mac_deframer::sptr
mac_deframer::make() {
	return gnuradio::get_initial_sptr(new mac_deframer_impl());
}


