LIBS :=
LIBS += libauth
LIBS += libdatetime
LIBS += libdb
LIBS += libenv
LIBS += libgemini
LIBS += libhash
LIBS += libhtml_table
LIBS += libnotify
LIBS += libopenai
LIBS += libplot
LIBS += libwebdriver

.PHONY: clone

clone: $(LIBS)

lib%:
	@[ ! -d '$@' ] && git clone git@github.com:gunchul/$@.git
