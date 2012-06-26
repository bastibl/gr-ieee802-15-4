CONTIKI = ../../contiki

ifndef TARGET
TARGET=sky
endif

CFLAGS += -DPROJECT_CONF_H=\"project-conf.h\"

all: sdr

upload:
	make sdr.upload

include $(CONTIKI)/Makefile.include
