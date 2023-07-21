# Copyright 2023 Ryan Volz
#
# This file is part of gr-ieee802_11
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

install(
    FILES ieee802_15_4_CSS_PHY.grc
          ieee802_15_4_OQPSK_PHY.grc
          transceiver_CSS_loopback.grc
          transceiver_CSS_USRP.grc
          transceiver_OQPSK.grc
    DESTINATION ${GR_PKG_DATA_DIR}/examples)
