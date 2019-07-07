from enum import Enum
import json, re
from datetime import datetime, timedelta

INVALID_JSON = "invalid json" 
INVALID_TRANS = "invalid transmitter"
INVALID_AGE = "invalid age"
INVALID_TYPE = "invalid type"

MSG_TYPE_83 = "83"
MSG_TYPE_84 = "84"
MSG_TYPE_0000 = "0000"

VALID_TYPES = [MSG_TYPE_83,MSG_TYPE_84,MSG_TYPE_0000]

msg_list = [
    '{"transmitter": "abc:123456","msg_time": "2019-03-15T10:26:37.951Z","msg_type": "83","message": "Hello World 83"}',
    '{"transmitter": "abc:123456","msg_time": "2019-03-15T10:26:37.951Z","msg_type": "84","message": "Hello World 84"}',
    '{"transmitter": "abc:123456","msg_time": "2019-03-15T10:26:37.951Z","msg_type": "0000","message": "Hello World 0000"}',

    '{"transmitter": "Qabc:123456","msg_time": "2019-03-15T10:26:37.951Z","msg_type": "83","message": "bad transmitter"}',
    '{"transmitter": "abc123456","msg_time": "2019-03-15T10:26:37.951Z","msg_type": "84","message": "bad transmitter"}',
    '{"transmitter": "abc:A123456","msg_time": "2019-03-15T10:26:37.951Z","msg_type": "84","message": "bad transmitter"}',

    '{"transmitter": "abc:A123456","msg_time": "2020-03-15T10:26:37.951Z","msg_type": "84","message": "bad date"}',
    '{"transmitter": "abc:A123456","msg_time": "2020-03-15T10:26:37.951Z","msg_type": "123","message": "bad type"}'
]

msg_type_0000_list = []
msg_type_83_list = []
msg_type_84_list = []
invalid_msg_list = []
        
def is_valid_transmitter(transmitter):
    try:
        m = re.match(r'^.{3}:\d*$', transmitter) # note, \d does not much uniq digit strings (like ٠١٢٣٤٥٦٧٨٩)
        return m is not None
    except Exception as e:
        return False
        

def is_older_than_7_days(date):
    time_between = datetime.now() - datetime.strptime(date,'%Y-%m-%dT%X.%fZ')
    return time_between.days > 7

def is_valid_type(type):
    return str(type) in VALID_TYPES

# Validation loop
for msg in msg_list:
    # check if valid json
    try:
        msg = json.loads(msg)
    except Exception as e:
        invalid_msg_list.append({
            "message": msg,
            "reason": INVALID_JSON
        })
    
    if not is_valid_transmitter(msg['transmitter']):
        invalid_msg_list.append({
            "message": msg,
            "reason": INVALID_TRANS
        })
    
    elif not is_older_than_7_days(msg['msg_time']):
        invalid_msg_list.append({
            "message": msg,
            "reason": INVALID_AGE
        })

    elif not is_valid_type(msg['msg_type']):
        invalid_msg_list.append({
            "message": msg,
            "reason": INVALID_TYPE
        })

    else: 
        type = str(msg['msg_type'])
        if type == MSG_TYPE_83:
            msg_type_83_list.append(msg)
        elif type == MSG_TYPE_84:
            msg_type_84_list.append(msg)
        elif type == MSG_TYPE_0000:
            msg_type_0000_list.append(msg)


print("0000 msg's: %s\n" % str(msg_type_0000_list))
print("83 msg's: %s\n" % str(msg_type_83_list))
print("84 msg's: %s\n" % str(msg_type_84_list))
print("invalid msg's: %s\n" % str(invalid_msg_list))