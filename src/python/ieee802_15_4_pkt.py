#
# Copyright 2005 Free Software Foundation, Inc.
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

# This is derived from gmsk2_pkt.py.
#
# Modified by: Thomas Schmid, Leslie Choong, Sanna Leidelof
#

import Numeric

from gnuradio import gr, packet_utils, gru
from gnuradio import ucla
import crc16
import gnuradio.gr.gr_threading as _threading
import ieee802_15_4
import struct

MAX_PKT_SIZE = 128

def make_ieee802_15_4_packet(FCF, seqNr, addressInfo, payload, pad_for_usrp=True, preambleLength=4, SFD=0xA7):
    """
    Build a 802_15_4 packet

    @param FCF: 2 bytes defining the type of frame.
    @type FCF: string
    @param seqNr: 1 byte sequence number.
    @type seqNr: byte
    @param addressInfo: 0 to 20 bytes of address information.
    @type addressInfo: string
    @param payload: The payload of the packet. The maximal size of the message
    can not be larger than 128.
    @type payload: string
    @param pad_for_usrp: If we should add 0s at the end to pad for the USRP.
    @type pad_for_usrp: boolean
    @param preambleLength: Length of the preambble. Currently ignored.
    @type preambleLength: int
    @param SFD: Start of frame describtor. This is by default set to the IEEE 802.15.4 standard,
    but can be changed if required.
    @type SFD: byte
    """

    if len(FCF) != 2:
        raise ValueError, "len(FCF) must be equal to 2"
    if seqNr > 255:
        raise ValueError, "seqNr must be smaller than 255"
    if len(addressInfo) > 20:
        raise ValueError, "len(addressInfo) must be in [0, 20]"

    if len(payload) > MAX_PKT_SIZE - 5 - len(addressInfo):
        raise ValueError, "len(payload) must be in [0, %d]" %(MAX_PKT_SIZE)

    SHR = struct.pack("BBBBB", 0, 0, 0, 0, SFD)
    PHR = struct.pack("B", 3 + len(addressInfo) + len(payload) + 2)
    MPDU = FCF + struct.pack("B", seqNr) + addressInfo + payload
    crc = crc16.CRC16()
    crc.update(MPDU)

    FCS = struct.pack("H", crc.intchecksum())

    pkt = ''.join((SHR, PHR, MPDU, FCS))

    if pad_for_usrp:
        # note that we have 16 samples which go over the USB for each bit
        pkt = pkt + (_npadding_bytes(len(pkt), 8) * '\x00')+0*'\x00'

    return pkt

def _npadding_bytes(pkt_byte_len, spb):
    """
    Generate sufficient padding such that each packet ultimately ends
    up being a multiple of 512 bytes when sent across the USB.  We
    send 4-byte samples across the USB (16-bit I and 16-bit Q), thus
    we want to pad so that after modulation the resulting packet
    is a multiple of 128 samples.

    @param ptk_byte_len: len in bytes of packet, not including padding.
    @param spb: samples per baud == samples per bit (1 bit / baud with GMSK)
    @type spb: int

    @returns number of bytes of padding to append.
    """
    modulus = 128
    byte_modulus = gru.lcm(modulus/8, spb) / spb
    r = pkt_byte_len % byte_modulus
    if r == 0:
        return 0
    return byte_modulus - r

def make_FCF(frameType=1, securityEnabled=0, framePending=0, acknowledgeRequest=0, intraPAN=0, destinationAddressingMode=0, sourceAddressingMode=0):
    """
    Build the FCF for the 802_15_4 packet

    """
    if frameType >= 2**3:
        raise ValueError, "frametype must be < 8"
    if securityEnabled >= 2**1:
        raise ValueError, " must be < "
    if framePending >= 2**1:
        raise ValueError, " must be < "
    if acknowledgeRequest >= 2**1:
        raise ValueError, " must be < "
    if intraPAN >= 2**1:
        raise ValueError, " must be < "
    if destinationAddressingMode >= 2**2:
        raise ValueError, " must be < "
    if sourceAddressingMode >= 2**2:
        raise ValueError, " must be < "



    return struct.pack("H", frameType
                       + (securityEnabled << 3)
                       + (framePending << 4)
                       + (acknowledgeRequest << 5)
                       + (intraPAN << 6)
                       + (destinationAddressingMode << 10)
                       + (sourceAddressingMode << 14))


class ieee802_15_4_mod_pkts(gr.hier_block2):
    """
    IEEE 802.15.4 modulator that is a GNU Radio source.

    Send packets by calling send_pkt
    """
    def __init__(self, pad_for_usrp=True, *args, **kwargs):
        """
	Hierarchical block for the 802_15_4 O-QPSK  modulation.

        Packets to be sent are enqueued by calling send_pkt.
        The output is the complex modulated signal at baseband.

        @param msgq_limit: maximum number of messages in message queue
        @type msgq_limit: int
        @param pad_for_usrp: If true, packets are padded such that they end up a multiple of 128 samples

        See 802_15_4_mod for remaining parameters
        """
	try:
		self.msgq_limit = kwargs.pop('msgq_limit')
	except KeyError:
		pass

	gr.hier_block2.__init__(self, "ieee802_15_4_mod_pkts",
				gr.io_signature(0, 0, 0),  # Input
				gr.io_signature(1, 1, gr.sizeof_gr_complex))  # Output
        self.pad_for_usrp = pad_for_usrp

        # accepts messages from the outside world
        self.pkt_input = gr.message_source(gr.sizeof_char, self.msgq_limit)
        self.ieee802_15_4_mod = ieee802_15_4.ieee802_15_4_mod(self, *args, **kwargs)
        self.connect(self.pkt_input, self.ieee802_15_4_mod, self)

    def send_pkt(self, seqNr, addressInfo, payload='', eof=False):
        """
        Send the payload.

        @param seqNr: sequence number of packet
        @type seqNr: byte
        @param addressInfo: address information for packet
        @type addressInfo: string
        @param payload: data to send
        @type payload: string
        """

        if eof:
            msg = gr.message(1) # tell self.pkt_input we're not sending any more packets
        else:
            FCF = make_FCF()

            pkt = make_ieee802_15_4_packet(FCF,
                                           seqNr,
                                           addressInfo,
                                           payload,
                                           self.pad_for_usrp)
             #print "pkt =", packet_utils.string_to_hex_list(pkt), len(pkt)
            msg = gr.message_from_string(pkt)
        self.pkt_input.msgq().insert_tail(msg)


class ieee802_15_4_demod_pkts(gr.hier_block2):
    """
    802_15_4 demodulator that is a GNU Radio sink.

    The input is complex baseband.  When packets are demodulated, they are passed to the
    app via the callback.
    """

    def __init__(self, *args, **kwargs):
        """
	Hierarchical block for O-QPSK demodulation.

	The input is the complex modulated signal at baseband.
        Demodulated packets are sent to the handler.

        @param callback:  function of two args: ok, payload
        @type callback: ok: bool; payload: string
        @param threshold: detect access_code with up to threshold bits wrong (-1 -> use default)
        @type threshold: int

        See ieee802_15_4_demod for remaining parameters.
	"""
	try:
		self.callback = kwargs.pop('callback')
		self.threshold = kwargs.pop('threshold')
		self.chan_num = kwargs.pop('channel')
	except KeyError:
		pass

	gr.hier_block2.__init__(self, "ieee802_15_4_demod_pkts",
				gr.io_signature(1, 1, gr.sizeof_gr_complex),  # Input
				gr.io_signature(0, 0, 0))  # Output

        self._rcvd_pktq = gr.msg_queue()          # holds packets from the PHY
        self.ieee802_15_4_demod = ieee802_15_4.ieee802_15_4_demod(self, *args, **kwargs)
        self._packet_sink = ucla.ieee802_15_4_packet_sink(self._rcvd_pktq, self.threshold)

        self.connect(self,self.ieee802_15_4_demod, self._packet_sink)

        self._watcher = _queue_watcher_thread(self._rcvd_pktq, self.callback, self.chan_num)

    def carrier_sensed(self):
        """
        Return True if we detect carrier.
        """
        return self._packet_sink.carrier_sensed()


class _queue_watcher_thread(_threading.Thread):
    def __init__(self, rcvd_pktq, callback, chan_num):
        _threading.Thread.__init__(self)
        self.setDaemon(1)
        self.rcvd_pktq = rcvd_pktq
        self.callback = callback
        self.chan_num = chan_num
        self.prev_crc = -1
        self.keep_running = True
        self.start()

    def run(self):
        while self.keep_running:
            print "802_15_4_pkt: waiting for packet"
            msg = self.rcvd_pktq.delete_head()
            ok = 0
            payload = msg.to_string()

            print "received packet "
            if len(payload) > 2:
                crc = crc16.CRC16()
            else:
                print "too small:", len(payload)
                continue
            # Calculate CRC skipping over LQI and CRC
            crc.update(payload[1:-2])

            crc_check = crc.intchecksum()
            print "checksum: %s, received: %s" % (crc_check,
                        str(ord(payload[-2]) + ord(payload[-1])*256))
            ok = (crc_check == ord(payload[-2]) + ord(payload[-1])*256)
            msg_payload = payload

            if self.prev_crc != crc_check:
                self.prev_crc = crc_check
                if self.callback:
                    self.callback(ok, msg_payload, self.chan_num)

class chan_802_15_4:
    chan_map= { 11 : 2405e6,
        12 : 2410e6,
        13 : 2415e6,
        14 : 2420e6,
        15 : 2425e6,
        16 : 2430e6,
        17 : 2435e6,
        18 : 2440e6,
        19 : 2445e6,
        20 : 2450e6,
        21 : 2455e6,
        22 : 2460e6,
        23 : 2465e6,
        24 : 2470e6,
        25 : 2475e6,
        26 : 2480e6}
