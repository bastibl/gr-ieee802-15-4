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
#include <gnuradio/thread/thread.h>
#include <boost/random/uniform_int.hpp>
#include <boost/random/mersenne_twister.hpp>
#include <iostream>
#include <iomanip>

#include "shcs_mac_impl.h"
#include "shcs_ieee802154.h"

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
    shcs_mac_impl::shcs_mac_impl(bool debug, bool nwk_dev_type) :
    block ("shcs_mac",
          gr::io_signature::make(0, 0, 0),
          gr::io_signature::make(0, 0, 0)),
          d_msg_offset(0),
          d_seq_nr(0),
          d_debug(debug),
          d_num_packet_errors(0),
          d_num_packets_received(0),
          d_nwk_dev_type(nwk_dev_type)
    {
      /* Print hello message and time stamp */
      dout << "Hello, this is SHCS MAC protocol implementation, version 0.0.7" << endl;
      dout << "NWK device type: " << (nwk_dev_type==SUC ? "SU Coordinator" : "SU") << endl;

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

      /* Initialize channels list */
      for (int count = 1; count < num_of_channels; count++) {
          center_freqs[count] = center_freqs[count - 1] + channel_step;
      }

      GR_LOG_INFO(d_logger, "List of operating channels and center freq.: ");
      for (int count = 0; count < num_of_channels; count++) {
          GR_LOG_INFO(d_logger, boost::format{"%d: %e (Hz)"} % (count + 11)
                      % center_freqs[count] );
      }

      /* Create control threads */
      if (nwk_dev_type == SUC) {
          /* Create control thread for Coordinator */
          control_thread_ptr = boost::shared_ptr<gr::thread::thread>
                  (new gr::thread::thread(boost::bind(&shcs_mac_impl::coor_control_thread, this)));
      }
      else {
          /* Create control thread for SU */
          control_thread_ptr = boost::shared_ptr<gr::thread::thread>
                  (new gr::thread::thread(boost::bind(&shcs_mac_impl::su_control_thread, this)));
      }

    }

    /*------------------------------------------------------------------------*/
    shcs_mac_impl::~shcs_mac_impl()
    {
      GR_LOG_DEBUG(d_logger, "Destructor called.");
    }

    /*------------------------------------------------------------------------*/
    void shcs_mac_impl::coor_control_thread(void) {
      GR_LOG_DEBUG(d_logger, "Coordinator control thread created.");

      /* Waiting for everything to settle */
      boost::this_thread::sleep_for(boost::chrono::seconds{3});

      /* TODO: perform an energy scan to all channels and select the channel
       * with the least measured energy.
       * Currently, choose a random channel to set up network.
       */
      GR_LOG_DEBUG(d_logger, "Performing energy scan...");

      boost::random::mt19937 rng;
      boost::random::uniform_int_distribution<> channel_dist(0, num_of_channels-1);
      int working_channel = channel_dist(rng);
      GR_LOG_DEBUG(d_logger, boost::format("Working channel: %d (%e)")
        % (working_channel + 11) % center_freqs[working_channel]);

      /* Setup working channel on USRP */
      /* TODO: dict is not working, still no idea why (2017.06.11) */
//      pmt::pmt_t command = pmt::make_dict();
//      pmt::dict_add(command, pmt::mp("freq"), pmt::mp(center_freqs[working_channel]));
//      pmt::dict_add(command, pmt::mp("bandwidth"), pmt::mp(bandwidth));
//      pmt::dict_add(command, pmt::mp("rate"), pmt::mp(sampling_rate));

      pmt::pmt_t command = pmt::cons(
          pmt::mp("freq"),
          pmt::mp(center_freqs[working_channel])
      );

      message_port_pub(pmt::mp("usrp sink cmd"), command);
      message_port_pub(pmt::mp("usrp source cmd"), command);

      /* TODO: Perform sensing, currently assume the current channel is available */

      /* Broadcast beacon */
      GR_LOG_DEBUG(d_logger, "Preparing beacon.");

      uint8_t mhr[IEEE802154_MAX_HDR_LEN];
      uint8_t flags = IEEE802154_FCF_TYPE_BEACON;
      size_t mhr_len = 0;
      le_uint16_t pan_id_le = byteorder_btols(byteorder_htons(pan_id));

      if ((mhr_len = ieee802154_set_frame_hdr(mhr, NULL, 0, NULL, 0, pan_id_le,
                                              pan_id_le, flags, d_seq_nr)) == 0) {
          GR_LOG_DEBUG(d_logger, "Beacon header error.");
      }
      else {
          GR_LOG_DEBUG(d_logger, )
      }

      int heartbeat = 0;
      while (1) {
          boost::this_thread::sleep_for(boost::chrono::seconds{1});
          GR_LOG_DEBUG(d_logger, boost::format("Time #%d") % heartbeat++);
      }

    }

    /*------------------------------------------------------------------------*/
    void shcs_mac_impl::su_control_thread(void) {
      GR_LOG_DEBUG(d_logger, "SU control thread created.");

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

