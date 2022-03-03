#!python
from load_json import jsonObject
import math

set_get_functions = ""
messages_list = []

for index, messages in enumerate(jsonObject["messages"]):
    message_struct = f'''{{{messages["id"]}, {math.ceil((messages["signals"][-1]["start"] + messages["signals"][-1]["length"])/8)}, {{0}}}}'''
    messages_list.append(message_struct)

    for signal in messages["signals"]:
        if "range" in signal:
            low_boundarie = str(signal["range"][0])
            high_boundarie = str(signal["range"][1])

        if "status" in signal.values():
            low_boundarie = jsonObject["defines"]["status"][0]
            high_boundarie = jsonObject["defines"]["status"][2]

        if "states" in signal.values():
            low_boundarie = jsonObject["defines"]["states"][0]
            high_boundarie = jsonObject["defines"]["states"][1]

        if signal.get("type") == "float":
            if_float_multiply = '''\n\t\tvalue *= 10;'''
            if_float_devide = "\n\tvalue /= 10;"
        else:
            if_float_multiply = ""
            if_float_devide = ""
        set = \
            f"""
bool canbus_set_{signal.get("name")}({signal.get("type")} value)
{{
    bool status = false;

    if ({low_boundarie} <= value && value <= {high_boundarie})
    {{\
        {if_float_multiply}
        buffer_insert(messages[{index}].buf, {signal.get("start")}, {signal.get("length")}, value);
        status = true;
    }}

    return status;
}}
              """  # string of doxygen text for set functions

        get = \
            f"""
{signal.get("type")} canbus_get_{signal.get("name")}(void)
{{
    {signal.get("type")} value = 0;
    value = ({signal.get("type")})buffer_extract(messages[{index}].buf, {signal.get("start")}, {signal.get("length")});\
    {if_float_devide}
    return value; 
}}
              """  # string of doxygen text for get functions

        set_get_functions += set + get
        # adds all the doxygen comments and functions to set_and_get.
