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

#####################################################################
# Setup library
#####################################################################
include(GrPlatform) #define LIB_SUFFIX

list(APPEND gr_ieee802_15_4_sources
    access_code_prefixer.cc
    bc_connection.cc
    mac.cc
    packet_sink.cc
    rime_connection.cc
    rime_stack.cc
    ruc_connection.cc
    stubborn_sender.cc
    uc_connection.cc
)

list(APPEND gr_ieee802_15_4_libs
    ${Boost_LIBRARIES}
    ${GNURADIO_ALL_LIBRARIES}
)

add_library(gnuradio-ieee802_15_4 SHARED ${gr_ieee802_15_4_sources})
target_link_libraries(gnuradio-ieee802_15_4 ${gr_ieee802_15_4_libs})
set_target_properties(gnuradio-ieee802_15_4 PROPERTIES DEFINE_SYMBOL "gnuradio_ieee802_15_4_EXPORTS")


if(APPLE)
    set_target_properties(gnuradio-ieee802_15_4 PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)


#####################################################################
# Install built library files
#####################################################################
install(TARGETS gnuradio-ieee802_15_4
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)
