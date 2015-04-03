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
# Setup python install
#####################################################################
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
endif()

list(APPEND python_sources
    __init__.py
    css_constants.py
    css_phy.py
    css_mod.py
    css_demod.py
)
GR_PYTHON_INSTALL(
    FILES ${python_sources}
    DESTINATION ${GR_PYTHON_DIR}/ieee802_15_4
    COMPONENT "ieee802_15_4_python"
)

#####################################################################
# Handle the unit tests
#####################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-ieee802-15-4)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)
GR_ADD_TEST(qa_phr_prefixer ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_phr_prefixer.py)
GR_ADD_TEST(qa_zeropadding_b ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_zeropadding_b.py)
GR_ADD_TEST(qa_codeword_mapper_bi ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_codeword_mapper_bi.py)
GR_ADD_TEST(qa_interleaver_ii ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_interleaver_ii.py)
GR_ADD_TEST(qa_qpsk_mapper_if ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_qpsk_mapper_if.py)
GR_ADD_TEST(qa_dqpsk_mapper_ff ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dqpsk_mapper_ff.py)
GR_ADD_TEST(qa_dqcsk_mapper_fc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dqcsk_mapper_fc.py)
GR_ADD_TEST(qa_preamble_sfd_prefixer_ii ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_preamble_sfd_prefixer_ii.py)
GR_ADD_TEST(qa_dqcsk_demapper_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dqcsk_demapper_cc.py)
GR_ADD_TEST(qa_qpsk_demapper_fi ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_qpsk_demapper_fi.py)
GR_ADD_TEST(qa_codeword_demapper_ib ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_codeword_demapper_ib.py)
GR_ADD_TEST(qa_zeropadding_removal_b ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_zeropadding_removal_b.py)
GR_ADD_TEST(qa_phr_removal ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_phr_removal.py)
GR_ADD_TEST(qa_css_txrx ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_css_txrx.py)  

GR_ADD_TEST(qa_chips_to_bits_fb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_chips_to_bits_fb.py)
GR_ADD_TEST(qa_access_code_removal_b ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_access_code_removal_b.py)
GR_ADD_TEST(qa_dqpsk_soft_demapper_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dqpsk_soft_demapper_cc.py)
GR_ADD_TEST(qa_deinterleaver_ff ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_deinterleaver_ff.py)
GR_ADD_TEST(qa_codeword_soft_demapper_fb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_codeword_soft_demapper_fb.py)
GR_ADD_TEST(qa_frame_buffer_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_frame_buffer_cc.py)
GR_ADD_TEST(qa_css_sync ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_css_sync.py)
GR_ADD_TEST(qa_multiuser_chirp_detector_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_multiuser_chirp_detector_cc.py)
GR_ADD_TEST(qa_preamble_tagger_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_preamble_tagger_cc.py)
