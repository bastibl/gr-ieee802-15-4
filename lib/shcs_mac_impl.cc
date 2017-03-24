/* -*- c++ -*- */
/* 
 * Copyright 2017 Real-time and Embedded Systems Laboratory, KAIST, South Korea.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

/**
 * @file shcs_mac_impl.cpp
 * @author  Nhat Pham <nhatphd@kaist.ac.kr>, Real-time and Embedded Systems Lab
 * @version 1.0
 * @date 2017-03-13
 * @brief This is the implementation for SHCS MAC protocol.
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <gnuradio/block_detail.h>
#include <iostream>
#include <iomanip>

#include "shcs_mac_impl.h"

using namespace gr::ieee802_15_4;
using namespace std;

#define dout d_debug && cout

namespace gr {
  namespace ieee802_15_4 {

    /*------------------------------------------------------------------------*/
    shcs_mac::sptr shcs_mac::make(bool debug, bool nwk_dev_type)
    {
      return gnuradio::get_initial_sptr(new shcs_mac_impl(debug, nwk_dev_type));
    }

    /*------------------------------------------------------------------------*/
    shcs_mac_impl::shcs_mac_impl(bool debug, bool d_nwk_dev_type) :
    block ("shcs_mac",
          gr::io_signature::make(0, 0, 0),
          gr::io_signature::make(0, 0, 0)),
          d_msg_offset(0),
          d_seq_nr(0),
          d_debug(debug),
          d_num_packet_errors(0),
          d_num_packets_received(0),
          d_nwk_dev_type(d_nwk_dev_type)
    {
      /* Print hello message and time stamp */
      dout << "Hello, this is SHCS MAC protocol implementation, version 0.0.2" << endl;
      dout << "NWK device type: " << (d_nwk_dev_type==SUC ? "SUC" : "SU") << endl;

      /* Register message port from NWK Layer */
      message_port_register_in(pmt::mp("app in"));
      set_msg_handler(pmt::mp("app in"), boost::bind(&shcs_mac_impl::app_in, this, _1));

      /* Register message port from PHY Layer */
      message_port_register_in(pmt::mp("pdu in"));
      set_msg_handler(pmt::mp("pdu in"), boost::bind(&shcs_mac_impl::mac_in, this, _1));

      /* Register message port to NWK Layer */
      message_port_register_out(pmt::mp("app out"));

      /* Register message port to PHY Layer */
      message_port_register_out(pmt::mp("pdu out"));

      /* Register command message ports to USRP blocks */
      message_port_register_out(pmt::mp("usrp sink cmd"));
      message_port_register_out(pmt::mp("usrp source cmd"));


    }

    /*------------------------------------------------------------------------*/
    shcs_mac_impl::~shcs_mac_impl()
    {
    }


    /*------------------------------------------------------------------------*/
    void shcs_mac_impl::mac_in(pmt::pmt_t msg) {
      pmt::pmt_t blob;

      if(pmt::is_pair(msg)) {
        blob = pmt::cdr(msg);
      } else {
        assert(false);
      }

      size_t data_len = pmt::blob_length(blob);
      if(data_len < 11) {
        dout << "MAC: frame too short. Dropping!" << endl;
        return;
      }

      uint16_t crc = crc16((char*)pmt::blob_data(blob), data_len);
      d_num_packets_received++;
      if(crc) {
        d_num_packet_errors++;
        dout << "MAC: wrong crc. Dropping packet!" << endl;
        return;
      }
      else{
        dout << "MAC: correct crc. Propagate packet to APP layer." << endl;
      }

      pmt::pmt_t mac_payload = pmt::make_blob((char*)pmt::blob_data(blob) + 9 , data_len - 9 - 2);

      message_port_pub(pmt::mp("app out"), pmt::cons(pmt::PMT_NIL, mac_payload));
    }

    /*------------------------------------------------------------------------*/
    void shcs_mac_impl::app_in(pmt::pmt_t msg) {
      pmt::pmt_t blob;
      if(pmt::is_eof_object(msg)) {
        dout << "MAC: exiting" << endl;
        detail().get()->set_done(true);
        return;
      } else if(pmt::is_blob(msg)) {
        blob = msg;
      } else if(pmt::is_pair(msg)) {
        blob = pmt::cdr(msg);
      } else {
        dout << "MAC: unknown input" << endl;
        return;
      }

      dout << "MAC: received new message from APP of length " << pmt::blob_length(blob) << endl;

      generate_mac((const char*)pmt::blob_data(blob), pmt::blob_length(blob));
      print_message();
      message_port_pub(pmt::mp("pdu out"), pmt::cons(pmt::PMT_NIL,
          pmt::make_blob(d_msg, d_msg_len)));
    }

    /*------------------------------------------------------------------------*/
    uint16_t shcs_mac_impl::crc16(char *buf, int len) {
      uint16_t crc = 0;

      for(int i = 0; i < len; i++) {
        for(int k = 0; k < 8; k++) {
          int input_bit = (!!(buf[i] & (1 << k)) ^ (crc & 1));
          crc = crc >> 1;
          if(input_bit) {
            crc ^= (1 << 15);
            crc ^= (1 << 10);
            crc ^= (1 <<  3);
          }
        }
      }

      return crc;
    }

    /*------------------------------------------------------------------------*/
    void shcs_mac_impl::generate_mac(const char *buf, int len) {

      // FCF
      // data frame, no security
      d_msg[0] = 0x41;
      d_msg[1] = 0x88;

      // seq nr
      d_msg[2] = d_seq_nr++;

      // addr info
      d_msg[3] = 0xcd;
      d_msg[4] = 0xab;
      d_msg[5] = 0xff;
      d_msg[6] = 0xff;
      d_msg[7] = 0x40;
      d_msg[8] = 0xe8;

      memcpy(d_msg + 9, buf, len);

      uint16_t crc = crc16(d_msg, len + 9);

      d_msg[ 9 + len] = crc & 0xFF;
      d_msg[10 + len] = crc >> 8;

      d_msg_len = 9 + len + 2;
    }

    /*------------------------------------------------------------------------*/
    void shcs_mac_impl::print_message() {
      for(int i = 0; i < d_msg_len; i++) {
        dout << setfill('0') << setw(2) << hex << ((unsigned int)d_msg[i] & 0xFF) << dec << " ";
        if(i % 16 == 15) {
          dout << endl;
        }
      }
      dout << endl;
    }

    /*------------------------------------------------------------------------*/
    int shcs_mac_impl::get_num_packet_errors(){ return d_num_packet_errors; }

    /*------------------------------------------------------------------------*/
    int shcs_mac_impl::get_num_packets_received(){ return d_num_packets_received; }

    /*------------------------------------------------------------------------*/
    float shcs_mac_impl::get_packet_error_ratio(){ return float(d_num_packet_errors)/d_num_packets_received; }


  } /* namespace ieee802_15_4 */
} /* namespace gr */

