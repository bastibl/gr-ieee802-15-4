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
#include <gnuradio/ieee802_15_4/rime_deframer.h>

#include <gr_io_signature.h>
#include <gr_block_detail.h>
#include <string.h>

using namespace gr::ieee802_15_4;

class rime_deframer_impl : public rime_deframer {

public:

#define dout d_debug && std::cout

rime_deframer_impl(bool debug) : gr_block("rime_deframer",
		gr_make_io_signature (0, 0, 0),
		gr_make_io_signature (0, 0, 0)),
		d_debug(debug) {

	message_port_register_out(pmt::mp("pdu out"));

	message_port_register_in(pmt::mp("pdu in"));
	set_msg_handler(pmt::mp("pdu in"), boost::bind(&rime_deframer_impl::make_frame, this, _1));
}

~rime_deframer_impl() {

}

void make_frame (pmt::pmt_t msg) {

	pmt::pmt_t blob;

	if(pmt::pmt_is_eof_object(msg)) {
		message_port_pub(pmt::mp("pdu out"), pmt::PMT_EOF);
		detail().get()->set_done(true);
		return;
	} else if(pmt::pmt_is_pair(msg)) {
		blob = pmt::pmt_cdr(msg);
	} else {
		assert(false);
	}

	size_t data_len = pmt::pmt_blob_length(blob);

	pmt::pmt_t rime_payload = pmt::pmt_make_blob((char*)pmt::pmt_blob_data(blob) + 4, data_len - 4);

	message_port_pub(pmt::mp("pdu out"), pmt::pmt_cons(pmt::PMT_NIL, rime_payload));

	dout << std::string((char*)pmt::pmt_blob_data(blob) + 4, data_len - 4) << std::endl;
}

private:
	bool d_debug;
};

rime_deframer::sptr
rime_deframer::make(bool debug) {
	return gnuradio::get_initial_sptr(new rime_deframer_impl(debug));
}

