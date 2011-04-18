
PROJ = ping_app
ROOTDIR = ${SOS_DIR}

#DEFS += -DMICASB
SRCS += ping.c loader.c 

ifdef INTERVAL
DEFS += -DPING_TIMER_INTERVAL=$(INTERVAL)
endif

include $(ROOTDIR)/config/Makerules

vpath loader.c $(ROOTDIR)/modules/management/loader/
vpath ping.c ../../modules/ping/

