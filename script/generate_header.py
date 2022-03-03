from load_json import jsonObject

set_and_get = ""
macros = ""

for messages in jsonObject["messages"]:
    for signal in messages["signals"]:

        set = \
            f"""
/**
 * @brief This function is used to set {signal.get("comment")}.
 * @param value The value to set.
 * @return true if value is valid otherwise return false.
 */
bool canbus_set_{signal.get("name")}({signal.get("type")} value); 
              """  # string of doxygen text for set functions

        get = \
            f"""
/**
 * @brief This function is used to get {signal.get("comment")}.
 * @return {signal.get("type")} The extracted data.
 */
{signal.get("type")} canbus_get_{signal.get("name")}(void);
              """  # string of doxygen text for get functions

        set_and_get += set + get
        # adds all the doxygen comments and functions to set_and_get.
for defines in jsonObject["defines"]:
    for index, values in enumerate(jsonObject["defines"][defines]):

        define = f'''\
#define {values} {str(index)}
'''
        macros += define
