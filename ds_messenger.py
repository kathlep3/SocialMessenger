# Kathleen Pham
# kathlep3@uci.edu
# 79281883

"""
Module containing DirectMessenger class for sending
and retrieving messages using DS protocol.
"""

import socket
import json
from ds_protocol import directmessage, extract_json, join_act


class DirectMessage:
    '''This class holds attributes for sent messages'''

    def __init__(self):
        '''This holds variables for messages we will send'''
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    '''This class holds variables and functions
    for sending or requesting messages'''

    def __init__(self, dsuserver=None, username=None, password=None):
        '''This holds variables for the person sending and where'''
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.port = 3021

    def send_message(self, message: str, recipient: str) -> bool:
        '''This function sends a direct message,
        returns true if pass, false if fail'''
        port = self.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.dsuserver, port))

            send = client.makefile("w")
            recv = client.makefile("r")

            send_server = join_act(self.username, self.password)
            trans_mess = json.dumps(send_server)

            send.write(trans_mess)
            send.flush()

            srv_tuple = str(recv.readline())
            extracted_resp = extract_json(srv_tuple)
            e_response = extracted_resp[0]
            e_type = extracted_resp[1]

            if len(e_response) > 2:
                self.token = e_response['token']

            if e_type == 'ok':
                if message != '':
                    my_message = directmessage(self.token, message, recipient)
                    send_message = json.dumps(my_message)
                    send.write(send_message)
                    send.flush()
                    dm_response = recv.readline()
                    extracted_dm = extract_json(dm_response)
                    dm_message = extracted_dm[2]
                    print(dm_message)
                    print()
                    print(dm_response)
                    print()
                return True

            if e_type == 'error':
                return False

    def retrieve_new(self) -> list:
        '''returns a list of new messages as an instance of DirectMessage'''
        port = self.port
        new_messages = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.dsuserver, port))

            send = client.makefile("w")
            recv = client.makefile("r")

            send_server = join_act(self.username, self.password)
            trans_mess = json.dumps(send_server)

            send.write(trans_mess)
            send.flush()

            srv_tuple = str(recv.readline())
            extracted_resp = extract_json(srv_tuple)
            e_response = extracted_resp[0]
            e_type = extracted_resp[1]

            if len(e_response) > 2:
                self.token = e_response['token']

            if e_type == 'ok':
                message = 'new'
                my_message = directmessage(self.token, message)
                send_message = json.dumps(my_message)
                send.write(send_message)
                send.flush()
                dm_response = recv.readline()
                extracted_dm = extract_json(dm_response)
                for message in extracted_dm.messages:
                    dm = DirectMessage()
                    dm.message = message['from']
                    dm.recipient = message['message']
                    dm.timestamp = message['timestamp']
                    new_messages.append(dm)
        print(new_messages)
        return new_messages

    def retrieve_all(self) -> list:
        '''returns a list of all messages as an instance of DirectMessage'''
        port = self.port
        all_messages = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.dsuserver, port))

            send = client.makefile("w")
            recv = client.makefile("r")

            send_server = join_act(self.username, self.password)
            trans_mess = json.dumps(send_server)

            send.write(trans_mess)
            send.flush()

            srv_tuple = str(recv.readline())
            extracted_resp = extract_json(srv_tuple)
            e_response = extracted_resp[0]
            e_type = extracted_resp[1]

            if len(e_response) > 2:
                self.token = e_response['token']

            if e_type == 'ok':
                message = 'all'
                my_message = directmessage(self.token, message)
                send_message = json.dumps(my_message)
                send.write(send_message)
                send.flush()
                dm_response = recv.readline()
                extracted_dm = extract_json(dm_response)
                for message in extracted_dm.messages:
                    dm = DirectMessage()
                    dm.message = message['from']
                    dm.recipient = message['message']
                    dm.timestamp = message['timestamp']
                    all_messages.append(dm)
        print(all_messages)
        return all_messages


# if __name__ == "__main__":
#     server = "168.235.86.101"
#     username = "katpham"
#     password = "mypass"
#     message = "Does this work"
#     recipient = "katpham"
#     dmEr = DirectMessenger(server, username, password)
#     test1 = dmEr.send_message(message, recipient)
#     test2 = dmEr.retrieve_new()
#     test3 = dmEr.retrieve_all()
