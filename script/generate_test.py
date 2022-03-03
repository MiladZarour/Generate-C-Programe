#!python
from load_json import jsonObject
"""
i. A valid value in the range/values specified in the signal
ii. The boundaries specified in the range/values
iii. An invalid value(s) which are out of the range/values
"""
functions = ""
run_tests = ""

for messages in jsonObject["messages"]:
    for signal in messages["signals"]:

        if "_t" in signal.get("type"):
            x = -2
        else:
            x = len(signal.get("type"))

        if "range" in signal:
            valid_value = str(signal["range"][0] + 1)
            low_boundarie = str(signal["range"][0])
            high_boundarie = str(signal["range"][1])
            invalid_value = str(signal["range"][1] + 1)

        if "status" in signal.values():
            valid_value = jsonObject["defines"]["status"][1]
            low_boundarie = jsonObject["defines"]["status"][0]
            high_boundarie = jsonObject["defines"]["status"][2]
            invalid_value = jsonObject["defines"]["status"][2] + " + 1"

        if "states" in signal.values():
            low_boundarie = jsonObject["defines"]["states"][0]
            high_boundarie = jsonObject["defines"]["states"][1]
            invalid_value = jsonObject["defines"]["states"][1] + " + 1"
            valid_test = ""\

        else:
            valid_test = f'''
    TEST_ASSERT_TRUE(canbus_set_{signal.get("name")}({valid_value}));
    TEST_ASSERT_EQUAL_{signal.get("type")[:x].upper()}({valid_value}, canbus_get_{signal.get("name")}());
    '''

        test_functions = f'''\
void test_canbus_{signal.get("name")}()
{{\
    {valid_test}    
    TEST_ASSERT_TRUE(canbus_set_{signal.get("name")}({low_boundarie}));
    TEST_ASSERT_EQUAL_{signal.get("type")[:x].upper()}({low_boundarie}, canbus_get_{signal.get("name")}());

    TEST_ASSERT_TRUE(canbus_set_{signal.get("name")}({high_boundarie}));
    TEST_ASSERT_EQUAL_{signal.get("type")[:x].upper()}({high_boundarie}, canbus_get_{signal.get("name")}());

    TEST_ASSERT_FALSE(canbus_set_{signal.get("name")}({invalid_value}));
}}'''
        functions += test_functions + "\n\n"

        run_test = f'''RUN_TEST(test_canbus_{signal.get("name")});'''

        run_tests += f'''{run_test}
    '''
