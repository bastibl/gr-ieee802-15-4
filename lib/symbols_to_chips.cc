/*
 * Copyright 2004,2013 Free Software Foundation, Inc.
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

#include <gnuradio/ieee802_15_4/symbols_to_chips.h>
#include <iostream>
#include <gr_io_signature.h>

using namespace gr::ieee802_15_4;

static const unsigned int d_symbol_table[] = {
	3653456430,
	3986437410,
	786023250,
	585997365,
	1378802115,
	891481500,
	3276943065,
	2620728045,
	2358642555,
	3100205175,
	2072811015,
	2008598880,
	125537430,
	1618458825,
	2517072780,
	3378542520};

class symbols_to_chips_impl : public symbols_to_chips {

static const int TABLE_SIZE = 16;

public:
symbols_to_chips_impl() : gr_sync_interpolator("symbols_to_chips",
			gr_make_io_signature(1, 1, sizeof (unsigned char)),
			gr_make_io_signature(1, 1, sizeof (unsigned int)),
                        2)
{
}

~symbols_to_chips_impl() {
}

int work (int noutput_items, gr_vector_const_void_star& input_items,
		gr_vector_void_star& output_items) {

	const unsigned char *in = (const unsigned char*)input_items[0];
	unsigned int *out = (unsigned int*)output_items[0];

	for (int i = 0; i < noutput_items; i += 2){

		// The LSBlock is sent first (802.15.4 standard)
		memcpy(&out[i + 1], &d_symbol_table[(unsigned int)((in[i / 2] >> 4) & 0xF)], sizeof(unsigned int));
		memcpy(&out[i], &d_symbol_table[(unsigned int)(in[i / 2] & 0xF)], sizeof(unsigned int));
	}

	return noutput_items;
}
};

symbols_to_chips::sptr
symbols_to_chips::make() {
	return gnuradio::get_initial_sptr(new symbols_to_chips_impl());
}
