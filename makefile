# First we declare compiler, interpreter and flags options, then we select all the sub-directories used and the target output files

CC = gcc
CFLAGS = -g -Wall -Werror -Wextra
CDIRS = C
CTARGET = WsInput.out

PYTHON = python3
PYTHONFLAGS = -m
PYTESTFLAGS = -vv
PYTHONDIRS = Python
PYTHONTARGET = Python.run

ALLDIRS = $(CDIRS) $(PYTHONDIRS)

#set TEST to any other value to not run pytest
TEST = true

# For the C part of the program:
# We search within each CDIRS dir, and get the source files: dir/src/*.c.
# Then expand with the * wildcard: dir/src/file1.c, dir/src/file2.c, ...
# In two steps, we replace all /src/ to /obj/ in SRC and then extensions from .c to .o
# DEPS: dir/obj/file1.o, dir/obj/file2.o, ...
HEADERS = $(wildcard $(foreach dir, $(CDIRS), $(dir)/headers/*.h))
SRC = $(wildcard $(foreach dir, $(CDIRS), $(dir)/src/*.c))
DEPS = $(subst /src/,/obj/, $(SRC))
DEPS := $(patsubst %.c, %.o, $(DEPS))

all: $(CTARGET)

# This is how we compile all the C part of the code:
# For each C sub-directory, we use: make CC CFLAGS -C dir, to run the makefile from the subdirectory with the flags from this file
$(CTARGET):
# the '@' allows for each command not to show in the console, so we can decide what to show when the makefile is run
	@$(MAKE) info

# we use the recompile_flag file to know if any file in any subdirectory was compiled/recompiled or not
	@rm -f recompile_flag

# using the && operator allows us to execute the second command (i.e. create file) only if the first command goes well (returned 0)
# each sub-directory makefile returns 0 only if at least 1 object file was recompiled
	@$(foreach dir, $(CDIRS), -$(MAKE) CC="$(CC)" CFLAGS="$(CFLAGS)" -C $(dir) && touch recompile_flag;)

# we use bash to check if the recompile_flag file was created, to know if we have to compile the CTARGET output file or not
	@if test -f recompile_flag; then \
		echo $(CC) $(CFLAGS) -o $@ $(DEPS); \
		$(CC) $(CFLAGS) -o $@ $(DEPS); \
		echo "C compilation ended."; \
	else \
		echo "Compilation is not necessary."; \
	fi
	
	@rm -f recompile_flag

# make run compiles (if necessary), runs pytest and executes both parts of the project
run: $(CTARGET)
ifeq ($(TEST),true)
	@(pytest $(PYTESTFLAGS) $(PYTHONDIRS) && echo "Pytest ended successfully. Starting program.") || \
	(echo "Pytest failed during a test. Solve the problem or run with make run TEST=false"; exit 1)
else
	@echo "TEST flag disabled. Won't run pytest."
endif

	@echo "Starting C program (Input for the word search)."
	@./$(CTARGET)
	@echo "Starting Python program (Word search generator)."
	@$(PYTHON) $(PYTHONFLAGS) $(PYTHONTARGET)

# Again we use the makefile from each sub-directory to clean (in this case, both C and Python)
clean:
	@$(foreach dir, $(ALLDIRS), $(MAKE) clean -C $(dir);)
# We clean extra files that not depend on the sub-directories makefiles
	rm -f WsInput.out
	rm -rf .pytest_cache

# Shows general useful info
info:
	$(info ALLDIRS = $(ALLDIRS))
	$(info CDIRS = $(CDIRS))
	$(info SRC = $(SRC))
	$(info HEADERS = $(HEADERS))
	$(info DEPS = $(DEPS))
	$(info PYTHONDIRS = $(PYTHONDIRS))
	$(info PYTHONTARGET = $(PYTHONTARGET))
	$(info TEST = $(TEST))

.PHONY: all clean run info $(CTARGET)