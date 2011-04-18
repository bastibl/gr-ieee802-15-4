/* -*- Mode: C; tab-width:4 -*- */
/* ex: set ts=4 shiftwidth=4 softtabstop=4 cindent: */
/**
 * @brief simple module for testing radio
 */

/**
 * Module needs to include <module.h>
 */
#include <sys_module.h>
#include <module.h>
#define LED_DEBUG
#include <led_dbg.h>

#ifndef PING_TIMER_INTERVAL
#define PING_TIMER_INTERVAL	256L
#endif
#define PING_TID               0

#define PINGER_ID    DFLT_APP_ID0
#define MSG_TEST     MOD_MSG_START

/**
 * Module can define its own state
 */
typedef struct {
  uint8_t pid;
  uint8_t seq;
} app_state_t;

/**
 * Module state and ID declaration.
 * All modules should call the fallowing to macros to help the linker add
 * module specific meta data to the resulting binary image.  Note that the
 * parameters my be different.
 */

/**
 * Ping module
 *
 * @param msg Message being delivered to the module
 * @return int8_t SOS status message
 *
 * Modules implement a module function that acts as a message handler.  The
 * module function is typically implemented as a switch acting on the message
 * type.
 *
 * All modules should included a handler for MSG_INIT to initialize module
 * state, and a handler for MSG_FINAL to release module resources.
 */

static int8_t module(void *start, Message *e);

/**
 * This is the only global variable one can have.
 */
static mod_header_t mod_header SOS_MODULE_HEADER = {
  .mod_id         = DFLT_APP_ID0,
  .state_size     = sizeof(app_state_t),
  .num_timers     = 1,
  .num_sub_func   = 0,
  .num_prov_func  = 0,
  .platform_type  = HW_TYPE /* or PLATFORM_ANY */,
  .processor_type = MCU_TYPE,
  .code_id        = ehtons(DFLT_APP_ID0),
  .module_handler = module,
};


static int8_t module(void *state, Message *msg)
{
  /**
   * The module is passed in a void* that contains its state.  For easy
   * reference it is handy to typecast this variable to be of the
   * applications state type.  Note that since we are running as a module,
   * this state is not accessible in the form of a global or static
   * variable.
   */
  app_state_t *s = (app_state_t*)state;

  /**
   * Switch to the correct message handler
   */
  switch (msg->type){

	/**
	 * MSG_INIT is used to initialize module state the first time the
	 * module is used.  Many modules set timers at this point, so that
	 * they will continue to receive periodic (or one shot) timer events.
	 */
  case MSG_INIT:
	{
	  LED_DBG(LED_YELLOW_TOGGLE);
	  s->pid = msg->did;
	  /**
	   * The timer API takes the following parameters:
	   * - PID of the module the timer is for
	   * - Timer ID (used to distinguish multiple timers of different
	   *   ..types on the same host)
	   * - Type of timer
	   * - Timer delay in
	   */
	  DEBUG("Ping Start\n");
	  ker_timer_init(s->pid, PING_TID, TIMER_REPEAT);
	  ker_timer_start(s->pid, PING_TID, PING_TIMER_INTERVAL);
	  s->seq = 0;
	  break;
	}


	/**
	 * MSG_FINAL is used to shut modules down.  Modules should release all
	 * resources at this time and take care of any final protocol
	 * shutdown.
	 */
  case MSG_FINAL:
	{
	  /**
	   * Stop the timer
	   */
	  ker_timer_stop(s->pid, PING_TID);
	  DEBUG("Ping Stop\n");
	  break;
	}


	/**
	 * All timers addressed to this PID, regardless of the timer ID, are of
	 * type MSG_TIMER_TIMEOUT and handled by this handler.  Timers with
	 * different timer IDs can be further distinguished by testing for the
	 * type, as demonstrated in the relay module.
	 */
  case MSG_TIMER_TIMEOUT:
	{
	  MsgParam* params = (MsgParam*)(msg->data);

	  if (params->byte == PING_TID) {
		s->seq++;
		DEBUG("Ping Packet\n");
		LED_DBG(LED_YELLOW_TOGGLE);
		post_net(PINGER_ID, PINGER_ID, MSG_TEST, sizeof(s->seq), &(s->seq), SOS_MSG_HIGH_PRIORITY, BCAST_ADDRESS);
				
	  }
	  break;
	}
  case MSG_TEST:
	{
	  LED_DBG(LED_GREEN_TOGGLE);
	  DEBUG("Recv Packet\n");
	  break;
	}


	/**
	 * The default handler is used to catch any messages that the module
	 * does no know how to handle.
	 */
  default:
	return -EINVAL;
  }

  /**
   * Return SOS_OK for those handlers that have successfully been handled.
   */
  return SOS_OK;
}

#ifndef _MODULE_
mod_header_ptr ping_get_header()
{
  return sos_get_header_address(mod_header);
}
#endif

