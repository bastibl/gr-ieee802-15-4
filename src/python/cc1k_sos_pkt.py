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
# Modified by: Thomas Schmid
#

from math import pi
import Numeric

from gnuradio import gr, packet_utils
from gnuradio import ucla
import crc8
import gnuradio.gr.gr_threading as _threading
import cc1k
import struct

HEADER_SIZE = 8
MAX_PKT_SIZE = 128 - HEADER_SIZE

def make_sos_packet(am_group, module_src, module_dst, dst_addr, src_addr, msg_type, payload, sbp, access_code, pad_for_usrp=True):
    """
    Build a SOS packet

    @param am_group: 
    @param module_src:
    @param module_dst: 
    @param dst_addr:
    @param src_addr:
    @param msg_type:
    @param payload:
    @param sbp:
    @param access_code:
    @param pad_for_usrp:
    """

    if len(payload) > MAX_PKT_SIZE:
        raise ValueError, "len(payload) must be in [0, %d]" %(MAX_PKT_SIZE)

    header = ''.join((chr(am_group), chr(module_src), chr(module_dst), chr(dst_addr&0xFF), chr((dst_addr >> 8) & 0xFF), chr(src_addr&0xFF), chr((src_addr >> 8) & 0xFF), chr(msg_type&0xFF), chr((len(payload) & 0xFF))))
    
    crcClass = crc8.crc8()
    crc = struct.pack('H', crcClass.crc(header[1:]+payload))
    #crc = chr(0xfe)

    # create the packet with the syncronization header of 100x '10' in front.
    pkt = ''.join((20*struct.pack('B', 0xaa), access_code, header, payload, crc, 20*struct.pack('B', 0xaa)))

    return pkt

class cc1k_mod_pkts(gr.hier_block):
    """
    CC1K modulator that is a GNU Radio source.

    Send packets by calling send_pkt
    """
    def __init__(self, fg, access_code=None, msgq_limit=2, pad_for_usrp=True, *args, **kwargs):
        """
	Hierarchical block for the CC1K fsk  modulation.

        Packets to be sent are enqueued by calling send_pkt.
        The output is the complex modulated signal at baseband.

	@param fg: flow graph
	@type fg: flow graph
        @param access_code: 64-bit sync code
        @type access_code: string of length 8
        @param msgq_limit: maximum number of messages in message queue
        @type msgq_limit: int
        @param pad_for_usrp: If true, packets are padded such that they end up a multiple of 128 samples

        See cc1k_mod for remaining parameters
        """
        self.pad_for_usrp = pad_for_usrp
        if access_code is None:
            #this is 0x33CC
            access_code = struct.pack('BB', 0x33, 0xCC)

        #if not isinstance(access_code, str) or len(access_code) != 8:
        #    raise ValueError, "Invalid access_code '%r'" % (access_code,)
        self._access_code = access_code

        # accepts messages from the outside world
        self.pkt_input = gr.message_source(gr.sizeof_char, msgq_limit)
        self.cc1k_mod = cc1k.cc1k_mod(fg, *args, **kwargs)
        fg.connect(self.pkt_input, self.cc1k_mod)
        gr.hier_block.__init__(self, fg, None, self.cc1k_mod)

    def send_pkt(self, am_group, module_src, module_dst, dst_addr, src_addr, msg_type, payload='', eof=False):
        """
        Send the payload.

        @param payload: data to send
        @type payload: string
        """
        if eof:
            msg = gr.message(1) # tell self.pkt_input we're not sending any more packets
        else:
            #print "original_payload =", string_to_hex_list(payload)
            pkt = make_sos_packet(am_group,
                                  module_src,
                                  module_dst,
                                  dst_addr,
                                  src_addr,
                                  msg_type,
                                  payload,
                                  self.cc1k_mod.spb,
                                  self._access_code,
                                  self.pad_for_usrp)
            #print "pkt =", str(map(hex, map(ord, pkt)))
            msg = gr.message_from_string(pkt)
        self.pkt_input.msgq().insert_tail(msg)


class cc1k_demod_pkts(gr.hier_block):
    """
    cc1k demodulator that is a GNU Radio sink.

    The input is complex baseband.  When packets are demodulated, they are passed to the
    app via the callback.
    """

    def __init__(self, fg, access_code=None, callback=None, threshold=-1, *args, **kwargs):
        """
	Hierarchical block for binary FSK demodulation.

	The input is the complex modulated signal at baseband.
        Demodulated packets are sent to the handler.

	@param fg: flow graph
	@type fg: flow graph
        @param access_code: 64-bit sync code
        @type access_code: string of length 8
        @param callback:  function of two args: ok, payload
        @type callback: ok: bool; payload: string
        @param threshold: detect access_code with up to threshold bits wrong (-1 -> use default)
        @type threshold: int

        See cc1k_demod for remaining parameters.
	"""

        if access_code is None:
            #this is 0x999999995a5aa5a5
            access_code = chr(153) + chr(153) + chr(153) + chr(153) + chr(90) + chr(90) + chr(165) + chr(165)
        if not isinstance(access_code, str) or len(access_code) != 8:
            raise ValueError, "Invalid access_code '%r' len '%r'" % (access_code, len(access_code),)
        self._access_code = access_code

        self._rcvd_pktq = gr.msg_queue()          # holds packets from the PHY
        self.cc1k_demod = cc1k.cc1k_demod(fg, *args, **kwargs)
        self._packet_sink = ucla.sos_packet_sink(map(ord, access_code), self._rcvd_pktq, threshold)
        
        fg.connect(self.cc1k_demod, self._packet_sink)
        #filesink = gr.file_sink (gr.sizeof_char, "/tmp/rx.log")
        #fg.connect(self.cc1k_demod,filesink)
      
        gr.hier_block.__init__(self, fg, self.cc1k_demod, None)
        self._watcher = _queue_watcher_thread(self._rcvd_pktq, callback)

    def carrier_sensed(self):
        """
        Return True if we detect carrier.
        """
        return self._packet_sink.carrier_sensed()


class _queue_watcher_thread(_threading.Thread):
    def __init__(self, rcvd_pktq, callback):
        _threading.Thread.__init__(self)
        self.setDaemon(1)
        self.rcvd_pktq = rcvd_pktq
        self.callback = callback
        self.keep_running = True
        self.start()

    #def stop(self):
    #    self.keep_running = False
        
    def run(self):
        while self.keep_running:
            print "cc1k_sos_pkt: waiting for packet"
            msg = self.rcvd_pktq.delete_head()
            ok = 1
            payload = msg.to_string()
            
            #print "received packet "
            am_group = ord(payload[0])
            module_src = ord(payload[1])
            module_dst = ord(payload[2])
            dst_addr = ord(payload[4])*256 + ord(payload[3])
            src_addr = ord(payload[6])*256 + ord(payload[5])
            msg_type = ord(payload[7])
            msg_len = ord(payload[8])
            msg_payload = payload[9:9+msg_len]
            crc = ord(payload[-2]) + ord(payload[-1])*256

            crcClass = crc8.crc8()
            crcCheck = crcClass.crc(payload[1:9+msg_len])

            #print " bare msg: " + str(map(hex, map(ord, payload)))
            #print " am group: " + str(am_group)
            #print "  src_addr: "+str(src_addr)+" dst_addr: "+str(dst_addr)
            #print "  src_module: " + str(module_src) + " dst_module: " + str(module_dst)
            #print "  msg type: " + str(msg_type) + " msg len: " +str(msg_len)
            #print "  msg: " + str(map(hex, map(ord, msg_payload)))
            #print "  crc: " + str(crc)
            #print "  crc_check: " + str(crcCheck)
            #print
            ok = (crc == crcCheck)
            if self.callback:
                self.callback(ok, am_group, src_addr, dst_addr, module_src, module_dst, msg_type, msg_payload, crc)

