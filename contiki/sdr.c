/*
 * Copyright (C) 2013 Bastian Bloessl <bloessl@ccs-labs.org>
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
#include "contiki.h"
#include "dev/leds.h"
#include "dev/button-sensor.h"
#include "net/netstack.h"
#include "net/rime.h"
#include "net/rime/channel.h"
#include "net/rime/broadcast.h"
#include <stdio.h>

#define RADIO_CHANNEL 129

// dummy information that is sent
static const char payload[] = "Hello GNU Radio!\n";

PROCESS(spam_process, "spam process");
PROCESS(button_process, "button process");

AUTOSTART_PROCESSES(&button_process);

static void update_leds() {
	static uint8_t i = 0;
	i++;
	leds_off(LEDS_ALL);
	switch(i % 3) {
	case 0:
		leds_on(LEDS_RED);
		break;
	case 1:
		leds_on(LEDS_GREEN);
		break;
	case 2:
		leds_on(LEDS_BLUE);
		break;
	}
}

static void broadcastSent(struct broadcast_conn *c, int status, int num_tx) {
	update_leds();
}

static void broadcastReceived(struct broadcast_conn *c, const rimeaddr_t *from) {
	char *pkt = packetbuf_dataptr();
	static int8_t rssi;
	rssi = packetbuf_attr(PACKETBUF_ATTR_RSSI);

	printf("broadcast packet received from %d.%d with RSSI %d, LQI %u\n",
			from->u8[0], from->u8[1],
			rssi,
			packetbuf_attr(PACKETBUF_ATTR_LINK_QUALITY));

	printf("-------------------------------\n");
	int i;
	for(i = 0; i < packetbuf_datalen(); i++) {
		printf("%c", pkt[i]);
	}
	printf("-------------------------------\n");

}

static struct broadcast_conn broadcastConnection;
	static const struct broadcast_callbacks broadcastCallbacks = {
		broadcastReceived, broadcastSent
	};

/* periodic broadcast */
PROCESS_THREAD(spam_process, ev, data) {

	PROCESS_BEGIN();

	// init
	leds_off(LEDS_ALL);

	while(1) {
		// wait a bit
		static struct etimer et;
		etimer_set(&et, 1 * CLOCK_SECOND);
		PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));

		// send packet
		packetbuf_copyfrom(&payload, sizeof(payload));
		broadcast_send(&broadcastConnection);
	}

	PROCESS_END();
}

PROCESS_THREAD(button_process, ev, data) {

	PROCESS_BEGIN();
	SENSORS_ACTIVATE(button_sensor);

	static int stopped = 1;

	broadcast_open(&broadcastConnection, RADIO_CHANNEL, &broadcastCallbacks);

	while(1) {
		leds_off(LEDS_ALL);

		// wait for button press
		PROCESS_WAIT_EVENT_UNTIL(ev == sensors_event &&
				data == &button_sensor);

		if(stopped) {
			stopped = 0;
			process_start(&spam_process, NULL);
		} else {
			stopped = 1;
			process_exit(&spam_process);
		}
	}

	PROCESS_END();
}
