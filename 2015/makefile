	# ------------------------------
# Cross-platform Makefile
# ------------------------------

# Detect platform / pick tools
ifeq ($(OS),Windows_NT)
  EXE_EXT := .exe
  RM      := del /Q
  MKDIR   := if not exist bin mkdir bin
  RUNPFX  :=
else
  EXE_EXT :=
  RM      := rm -f
  MKDIR   := mkdir -p bin
  RUNPFX  := ./
endif

# Compiler & flags (override with: make CC=gcc CFLAGS="-Wall -O3")
CC      ?= clang
CFLAGS  ?= -Wall -O2
LDFLAGS ?=

# Add platform libs if needed
# (example: -lm on Linux)
UNAME_S := $(shell uname -s 2>/dev/null)
ifeq ($(UNAME_S),Linux)
  LDFLAGS += -lm
endif

# Days to build (no 'seq' on Windows)
DAYS := 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19

# Default target: build all days (pattern rule handles most)
.PHONY: all clean debug release
all: $(addprefix day,$(DAYS))

# Generic compile+run macro
# $(1)=dir like "01", $(2)=part "a"|"b", $(3)=extra args to run (optional)
define COMPILE_AND_RUN
	@echo ===== Day $(1)$(2) =====
	@$(MKDIR)
	@echo "$(CC) $(1)/$(2).c $(CFLAGS) $(LDFLAGS) -o bin/$(1)$(2)$(EXE_EXT)"
	@$(CC) $(1)/$(2).c $(CFLAGS) $(LDFLAGS) -o bin/$(1)$(2)$(EXE_EXT)
	@echo "$(RUNPFX)bin/$(1)$(2)$(EXE_EXT) $(3)"
	@$(RUNPFX)bin/$(1)$(2)$(EXE_EXT) $(3)
	@echo
endef

# Generic rule: dayXX builds & runs a and b with the default input
day%:
	$(call COMPILE_AND_RUN,$*,a,$*/input.txt)
	$(call COMPILE_AND_RUN,$*,b,$*/input.txt)

# -------------- Special cases --------------

# day04 needs OpenSSL and custom args
day04:
	@echo ===== Day 04 =====
	@$(MKDIR)
	@$(CC) 04/a.c $(CFLAGS) -lssl -lcrypto -o bin/04a$(EXE_EXT)
	@$(RUNPFX)bin/04a$(EXE_EXT) iwrupvqb
	@$(CC) 04/b.c $(CFLAGS) -lssl -lcrypto -o bin/04b$(EXE_EXT)
	@$(RUNPFX)bin/04b$(EXE_EXT) iwrupvqb
	@echo

day10:
	@echo ===== Day 10 =====
	@$(MKDIR)
	@$(CC) 10/a.c $(CFLAGS) -o bin/10a$(EXE_EXT)
	@$(RUNPFX)bin/10a$(EXE_EXT) 3113322113 40
	@$(RUNPFX)bin/10a$(EXE_EXT) 3113322113 50
	@echo

day11:
	@echo ===== Day 11 =====
	@$(MKDIR)
	@$(CC) 11/a.c $(CFLAGS) -o bin/11a$(EXE_EXT)
	@$(RUNPFX)bin/11a$(EXE_EXT) hepxcrrq
	@echo

day14:
	@echo ===== Day 14 =====
	@$(MKDIR)
	@$(CC) 14/a.c $(CFLAGS) -o bin/14a$(EXE_EXT)
	@$(RUNPFX)bin/14a$(EXE_EXT) 14/input.txt 2503
	@$(CC) 14/b.c $(CFLAGS) -o bin/14b$(EXE_EXT)
	@$(RUNPFX)bin/14b$(EXE_EXT) 14/input.txt 2503
	@echo

day15:
	@echo ===== Day 15 =====
	@$(MKDIR)
	@$(CC) 15/a.c $(CFLAGS) -o bin/15a$(EXE_EXT)
	@$(RUNPFX)bin/15a$(EXE_EXT) 15/input.txt
	@echo

day17:
	@echo ===== Day 17 =====
	@$(MKDIR)
	@$(CC) 17/a.c $(CFLAGS) -o bin/17a$(EXE_EXT)
	@$(RUNPFX)bin/17a$(EXE_EXT) 150 17/input.txt
	@$(CC) 17/b.c $(CFLAGS) -o bin/17b$(EXE_EXT)
	@$(RUNPFX)bin/17b$(EXE_EXT) 150 17/input.txt
	@echo

day18:
	@echo ===== Day 18 =====
	@$(MKDIR)
	@$(CC) 18/a.c $(CFLAGS) -o bin/18a$(EXE_EXT)
	@$(RUNPFX)bin/18a$(EXE_EXT) 100 100 18/input.txt
	@$(CC) 18/b.c $(CFLAGS) -o bin/18b$(EXE_EXT)
	@$(RUNPFX)bin/18b$(EXE_EXT) 100 100 18/input.txt
	@echo

day20:
	@echo ===== Day 20 =====
	@$(MKDIR)
	@$(CC) 20/a.c $(CFLAGS) $(LDFLAGS) -o bin/20a$(EXE_EXT)
	@$(RUNPFX)bin/20a$(EXE_EXT) 33100000
	# @$(CC) 18/b.c $(CFLAGS) -o bin/18b$(EXE_EXT)
	# @$(RUNPFX)bin/18b$(EXE_EXT) 100 100 18/input.txt
	@echo
# -------------- Utilities --------------

clean:
	@echo Cleaning...
	@$(RM) bin\*$(EXE_EXT) 2> NUL || true
	@$(RM) bin/*$(EXE_EXT) 2> /dev/null || true
	@echo Done.

debug:
	@$(MAKE) CFLAGS="-Wall -g -O0"

release:
	@$(MAKE) CFLAGS="-Wall -O3"
