/*
 * Copyright 2013 Free Software Foundation, Inc.
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
#define IEEE802_15_4_API

%include <gnuradio.i>

%include "ieee802_15_4_swig_doc.i"

%{
#include "ieee802_15_4/access_code_prefixer.h"
#include "ieee802_15_4/mac.h"
#include "ieee802_15_4/packet_sink.h"
#include "ieee802_15_4/rime_stack.h"
#include "ieee802_15_4/fragmentation.h"
#include "ieee802_15_4/phr_prefixer.h"
#include "ieee802_15_4/zeropadding_b.h"
#include "ieee802_15_4/codeword_mapper_bi.h"
#include "ieee802_15_4/interleaver_ii.h"
#include "ieee802_15_4/qpsk_mapper_if.h"
#include "ieee802_15_4/dqpsk_mapper_ff.h"
%}

%include "ieee802_15_4/access_code_prefixer.h"
%include "ieee802_15_4/mac.h"
%include "ieee802_15_4/packet_sink.h"
%include "ieee802_15_4/rime_stack.h"


GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, access_code_prefixer);
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, mac);
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, packet_sink);
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, rime_stack);

%include "ieee802_15_4/fragmentation.h"
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, fragmentation);
%include "ieee802_15_4/phr_prefixer.h"
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, phr_prefixer);
%include "ieee802_15_4/zeropadding_b.h"
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, zeropadding_b);
%include "ieee802_15_4/codeword_mapper_bi.h"
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, codeword_mapper_bi);
%include "ieee802_15_4/interleaver_ii.h"
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, interleaver_ii);
%include "ieee802_15_4/qpsk_mapper_if.h"
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, qpsk_mapper_if);
%include "ieee802_15_4/dqpsk_mapper_ff.h"
GR_SWIG_BLOCK_MAGIC2(ieee802_15_4, dqpsk_mapper_ff);
