#
# Copyright 2004,2005 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
# 

include $(top_srcdir)/Makefile.common

# Install this stuff so that it ends up as the gnuradio.ucla module
# This usually ends up at:
#   ${prefix}/lib/python${python_version}/site-packages/gnuradio

ourpythondir = $(grpythondir)
ourlibdir    = $(grpyexecdir)

INCLUDES = $(STD_DEFINES_AND_INCLUDES) $(PYTHON_CPPFLAGS)

SWIGCPPPYTHONARGS = -fvirtual -python -modern $(PYTHON_CPPFLAGS) \
	-I$(swigincludedir) -I$(grincludedir)

ALL_IFILES = 				\
	$(LOCAL_IFILES)			\
	$(NON_LOCAL_IFILES)		

NON_LOCAL_IFILES =			\
	$(GNURADIO_CORE_INCLUDEDIR)/swig/gnuradio.i


LOCAL_IFILES = 				\
	ucla.i

# These files are built by SWIG.  The first is the C++ glue.
# The second is the python wrapper that loads the _ucla shared library
# and knows how to call our extensions.

BUILT_SOURCES = 			\
	ucla.cc			\
	ucla.py				

# This gets ucla.py installed in the right place
ourpython_PYTHON =			\
	ucla.py

ourlib_LTLIBRARIES = _ucla.la

# These are the source files that go into the shared library
_ucla_la_SOURCES = 			\
	ucla.cc			        \
	ucla_cc1k_correlator_cb.cc      \
	ucla_sos_packet_sink.cc	        \
	ucla_ieee802_15_4_packet_sink.cc	\
	ucla_qpsk_modulator_cc.cc       \
	ucla_symbols_to_chips_bi.cc     \
	ucla_manchester_ff.cc     \
	ucla_multichanneladd_cc.cc          \
	ucla_delay_cc.cc

# magic flags
_ucla_la_LDFLAGS = $(NO_UNDEFINED) -module -avoid-version

# link the library against some comon swig runtime code and the 
# c++ standard library
_ucla_la_LIBADD = 			\
	$(PYTHON_LDFLAGS)		\
	-lstdc++			

ucla.cc ucla.py: ucla.i $(ALL_IFILES)
	$(SWIG) $(SWIGCPPPYTHONARGS) -module ucla -o ucla.cc $<

# These headers get installed in ${prefix}/include/gnuradio
grinclude_HEADERS =			\
	ucla_cc1k_correlator_cb.h       \
	ucla_sos_packet_sink.h          \
	ucla_ieee802_15_4_packet_sink.h       \
	ucla_qpsk_modulator_cc.h        \
	ucla_symbols_to_chips_bi.h      \
	ucla_manchester_ff.h      \
	ucla_multichanneladd_cc.h         \
	ucla_delay_cc.h


# These swig headers get installed in ${prefix}/include/gnuradio/swig
swiginclude_HEADERS = 			\
	$(LOCAL_IFILES)


MOSTLYCLEANFILES = $(BUILT_SOURCES) *.pyc

