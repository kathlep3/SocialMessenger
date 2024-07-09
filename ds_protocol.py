# ds_protocol.py

# Kathleen Pham
# kathlep3@uci.edu
# 79281883
'''This file is where the server response
is extracted from json to a namedtuple'''
import json
from collections import namedtuple


DataTuple = namedtuple('DataTuple', ['response',
                                     'type',
                                     'message',
                                     'messages'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string
    and convert it to a DataTuple object replace the
    pseudo placeholder keys with actual DSP protocol keys
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        typee = json_obj['response']['type']
        message = json_obj['response'].get('message')
        messages = json_obj['response'].get('messages')

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    return DataTuple(response, typee, message, messages)


def directmessage(token, entry, recipient=None):
    '''Send a directmessage to another DS user'''
    if recipient is not None:
        client_msg = {"token": token,
                      "directmessage": {"entry": entry,
                                        "recipient": recipient,
                                        "timestamp": "1603167689.3928561"}}
    elif entry == "new":
        client_msg = {"token": token, "directmessage": "new"}
    elif entry == "all":
        client_msg = {"token": token, "directmessage": "all"}
    else:
        print('Please use a valid request. (an entry, "new", or "all")')
    return client_msg


def join_act(username, password):
    '''Converts info to format to join server'''
    print("User joined.")
    print()
    client_msg = {"join": {"username": username,
                           "password": password,
                           "token": ""}}
    return client_msg


def post_act(new_post, token=None):
    '''Converts info to format to post to server for a3.py '''
    client_msg = {"token": token, "post": new_post}
    json_post = json.dumps(client_msg)
    return json_post


def bio_act(new_post, token=None):
    '''Converts info to format to post to server for a3.py'''
    client_msg = {"token": token,
                  "bio": {"entry": new_post,
                          "timestamp": ""}}
    json_bio = json.dumps(client_msg)
    return json_bio


# if __name__ == "__main__":
#     test = json.dumps({"response":
#                        {"type": "ok",
#                         "messages":
#                         [{"message":"Hello User 1!",
#                           "from":"markb",
#                           "timestamp":"1603167689.3928561"},
#                           {"message":"Bzzzzz",
#                            "from":"thebeemoviescript",
#                            "timestamp":"1603167689.3928561"}]}})
#     print(type(test))
#     print(test)
#     print()
#     ex_test = extract_json(test)
#     print(type(ex_test))
#     print(ex_test)
