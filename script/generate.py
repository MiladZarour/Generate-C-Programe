#!python
import os
from generate_test import functions, run_tests
from generate_header import set_and_get, macros
from generate_source import messages_list, set_get_functions

path_folder_test = "test/"
path_folder_canbus = "lib/canbus/"

path_file_test = "test/canbus_test.c"
path_file_header = "lib/canbus/canbus.h"
path_file_source = "lib/canbus/canbus.c"

# Check whether the test folder exists
test_folder_exist = os.path.exists(path_folder_test)
canbus_folder_exist = os.path.exists(path_folder_canbus)

if not test_folder_exist:
    # Create a new directory because it does not exist
    os.makedirs(path_folder_test)

if not canbus_folder_exist:
    # Create a new directory because it does not exist
    os.makedirs(path_folder_canbus)

if os.path.exists(path_file_test):  # Check whether the specified file exists
    os.remove(path_file_test)  # this deletes the file

if os.path.exists(path_file_header):  # Check whether the specified file exists
    os.remove(path_file_header)  # this deletes the file

if os.path.exists(path_file_source):  # Check whether the specified file exists
    os.remove(path_file_source)  # this deletes the file

with open(path_file_test, "a+") as f:
    # creates, opens and writes to a new file (canbus.h)
    f.write(f'''\
#include "unity.h"
#include "canbus.h"

void setUp(void) {{}}
void tearDown(void) {{}}

{functions}\

int main(void)
{{
    UNITY_BEGIN();

    {run_tests}\

    return UNITY_END();
}}''')

with open(path_file_header, "a+") as f:
    # creates, opens and writes to a new file (canbus.h)
    f.write(
        f"""\
#ifndef CANBUS_H
#define CANBUS_H

#include <stdint.h>
#include <stdbool.h>
{macros}
{set_and_get}
#endif /* CANBUS_H */\
""")

with open(path_file_source, "a+") as f:
    # creates, opens and writes to a new file (canbus.h)
    f.write(f'''\
#include "canbus.h"
#include "buffer.h"

typedef struct
{{
    uint32_t id;
    uint8_t len;
    uint8_t buf[8];
}}message_t;

static message_t messages[] = {{{", ".join(messages_list)}}};
{set_get_functions}\
''')
