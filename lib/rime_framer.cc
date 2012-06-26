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
#include <gnuradio/ieee802_15_4/rime_framer.h>

#include <gr_io_signature.h>
#include <gr_block_detail.h>
#include <string.h>

using namespace gr::ieee802_15_4;

class rime_framer_impl : public rime_framer {

public:

rime_framer_impl() : gr_block("rime_framer",
		gr_make_io_signature (0, 0, 0),
		gr_make_io_signature (0, 0, 0)) {

	message_port_register_out(pmt::mp("out"));

	message_port_register_in(pmt::mp("in"));
	set_msg_handler(pmt::mp("in"), boost::bind(&rime_framer_impl::make_frame, this, _1));

	buf[0] = 0x81;
	buf[1] = 0x00;
	buf[2] = 0x2a;
	buf[3] = 0x17;
}

~rime_framer_impl() {

}

void make_frame (pmt::pmt_t msg) {

        pmt::pmt_t blob;

	if(pmt::pmt_is_eof_object(msg)) {
		message_port_pub(pmt::mp("out"), pmt::PMT_EOF);
		detail().get()->set_done(true);
		return;
	} else if(pmt::pmt_is_pair(msg)) {
		blob = pmt::pmt_cdr(msg);
        } else if(pmt::pmt_is_symbol(msg)) {
		blob = pmt::pmt_make_blob(
			pmt::pmt_symbol_to_string(msg).data(),
			pmt::pmt_symbol_to_string(msg).length());
	} else if(pmt::pmt_is_blob(msg)) {
		blob = msg;
	} else {
		assert(false);
	}

	size_t data_len = pmt::pmt_blob_length(blob);
	assert(pmt::pmt_blob_length(blob));
	assert(data_len < 256 - 4);

	std::memcpy(buf + 4, pmt::pmt_blob_data(blob), data_len);
	pmt::pmt_t rime_msg = pmt::pmt_make_blob(buf, data_len + 4);

        message_port_pub(pmt::mp("out"), rime_msg);
}

private:
	char buf[256];

};

rime_framer::sptr
rime_framer::make() {
	return gnuradio::get_initial_sptr(new rime_framer_impl());
}


