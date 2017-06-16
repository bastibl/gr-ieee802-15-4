/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
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

#ifndef INCLUDED_IEEE802_15_4_SHCS_MAC_IMPL_H
#define INCLUDED_IEEE802_15_4_SHCS_MAC_IMPL_H

#include <ieee802_15_4/shcs_mac.h>


namespace gr {
  namespace ieee802_15_4 {

    class shcs_mac_impl : public shcs_mac
    {
     public:
      /**
       * @brief   Constructor.
       *
       * @param[in]   debug, turn on/off debugging messages.
       */
      shcs_mac_impl(bool debug, bool nwk_dev_type);

      /**
       * @brief   Destructor.
       *
       * @param[in]   debug, turn on/off debugging messages.
       */
      ~shcs_mac_impl();

      /**
       * @brief   Return number of error packets.
       *
       * @return  Number of error packets.
       */
      int get_num_packet_errors();

      /**
       * @brief   Return number of received packets.
       *
       * @return  Number of received packets.
       */
      int get_num_packets_received();

      /**
       * @brief   Return error ratio.
       *
       * @return  Error ratio.
       */
      float get_packet_error_ratio();

     /*--------------------------------- Private -----------------------------*/
     private:
       bool        d_debug;
       int         d_msg_offset;
       int         d_msg_len;
       uint8_t     d_seq_nr;
       char        d_msg[256];

       int d_num_packet_errors;
       int d_num_packets_received;

       /* network device type */
       bool       d_nwk_dev_type;

       /* wireless channel configuration */
       static const int num_of_channels = 2;  // channel 25 -> 26: [2.475, ..., 2.480] GHz,
       const double channel_step = 5e6; // 5MHz step between 2 channels.
       const int first_channel_index = 25;
       double center_freqs[num_of_channels] = {2.475e9}; // channel 25: 2.475GHz.

       const double bandwidth = 2e6;      // Hz, constant for LR-WPAN.
       const double sampling_rate = 4e6;  // Hz,

       const int Ts = 1000; // ms, slot duration (i.e. dwelling time of a channel hop).
       const int Tf = Ts*num_of_channels; // ms, frame duration.
       const uint16_t Tss = 1; // ms, sensing duration.

       const uint16_t pan_id = 0x1234; // just a random number, for now.
       const uint16_t suc_saddr = 0x0000; // Coordinator default address.
       const uint16_t su_saddr = 0x0101; // SU default address.
       uint16_t suc_rand_seed = 0;


       /* Control thread */
       boost::shared_ptr<gr::thread::thread> control_thread_ptr;

       /**
        * @brief   Control thread for Coordinator.
        */
       void coor_control_thread(void);

       /**
         * @brief   Control thread for SU.
         */
       void su_control_thread(void);

       /**
        * @brief   Handle package from PHY layer and forward processed package
        *          to upper layer.
        *
        * @param[in]   msg, message demodulated by PHY layer.
        */
       void mac_in(pmt::pmt_t msg);

      /**
       * @brief   Handle package from NETWORK layer and forward processed
       *          package to PHY layer.
       *
       * @param[in]   msg, message received from NETWORK layer.
       */
      void app_in(pmt::pmt_t msg);

      /**
       * @brief   Generate MAC frame from a received buffer.
       *
       * @param[in]   buf, buffer.
       * @param[in]   len, buffer length.
       */
      void generate_mac(const char *buf, int len);

      /**
       * @brief   Calculate CRC16 checksum for a buffer.
       *
       * @param[in]   buf, buffer.
       * @param[in]   len, buffer length.
       *
       * @return      crc16.
       */
      uint16_t crc16(char *buf, int len);

      /**
       * @brief   Print message in buffer.
       */
      void print_message();
    };

  } // namespace ieee802_15_4
} // namespace gr

#endif /* INCLUDED_IEEE802_15_4_SHCS_MAC_IMPL_H */

