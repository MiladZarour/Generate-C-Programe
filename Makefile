#a. You need to link the right object file in lib/buffer, depending on the OS
#b. In Makefile there shall be a check target to build and run canbus_test.c.
#c. In Makefile there shall be a generate target to run generate.py in order
#to generate the canbus module and canbus_test.c. 

OS_OBJ :=

ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    OS_OBJ := lib/buffer/windows.o
endif	
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	OS_OBJ := lib/buffer/macos.o
endif
ifeq ($(UNAME_S),Linux)
	OS_OBJ := lib/buffer/linux.o
endif

CC := gcc
CFLAGS := -Wall

LIB_DIR := lib
TEST_DIR := test
BUILD_DIR := build
CANBUS_DIR := lib/canbus

LIB_SRC := $(LIB_DIR)/*

TEST_EXE := test

INCLUDES := $(addprefix -I./,$(wildcard $(LIB_DIR)/*))

TEST_OBJS := $(notdir $(wildcard $(LIB_DIR)/*/*.c) $(wildcard $(TEST_DIR)/*.c))
TEST_OBJS := $(addprefix $(BUILD_DIR)/,$(TEST_OBJS:.c=.o))
OBJECTS := $(TEST_OBJS) $(OS_OBJ)

generate:
	@python script/generate.py
	@echo "************ The Targets ************"
	@echo "** clean: to clean"
	@echo "** check: build and run the test"
	@echo "*************************************"


$(TEST_EXE): $(OBJECTS)
	$(CC) $^ -o $(BUILD_DIR)/$@

$(BUILD_DIR)/%.o: $(LIB_SRC)/%.c
	$(CC) -MMD $(CFLAGS) -o $@ $(INCLUDES) -c $<

$(BUILD_DIR)/%.o : $(TEST_DIR)/%.c
	$(CC) -MMD $(CFLAGS) -o $@ $(INCLUDES) -c $<

check: mkbuild $(TEST_DIR)
	@echo "******************"
	@echo "***Run the test***"
	@echo "******************"
	@./$(BUILD_DIR)/$(TEST_EXE)

-include $(OBJECTS:.o=.d)

.PHONY: all mkbuild check clean generate

mkbuild:
	@mkdir -p $(BUILD_DIR)

clean:
	@rm -rf $(BUILD_DIR) $(TEST_DIR) $(CANBUS_DIR)
