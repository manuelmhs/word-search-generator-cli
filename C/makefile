# This makefile creates the object files in obj directory for each source file in src directory

# the wildcard expands to all files coincident with the pattern. * is replaced by any file name
HEADERS = $(wildcard headers/*.h)
SRC = $(wildcard src/*.c)
# in OBJ, we first replace ".c" with ".o", and then src/ with obj/, e.g:
# src/data.c -> src/data.o -> obj/data.o, in two steps
OBJ = $(subst src/, obj/, $(SRC:.c=.o))
# we use RETURNVAL to know if any obj file was recompiled or not
RETURNVAL = 2

# we recompile the obj files (if necessary) and then exit with RETURNVAL
all: $(OBJ)
	@exit $(RETURNVAL)

obj/%.o: src/%.c $(HEADERS)
# we use the compiler and flags passed to this makefile
	$(CC) $(CFLAGS) -c -o $@ $<
# we set RETURNVAL to 0, because at least 1 obj file was recompiled
	$(eval RETURNVAL = 0)

.PHONY: clean
clean:
	rm -f $(OBJ)