'''This file is meant to test functions from ds_protocol.py'''
import unittest
import json
from collections import namedtuple
from ds_protocol import directmessage, extract_json


class TestDSProtocol(unittest.TestCase):
    '''This is the test class using unittest'''

    def test_directmessage(self):
        '''This one tests direct message'''
        result = directmessage(
            entry="This is my entry,",
            token="c26ef69d-5a7b-4186-9700-471aa0faea7d",
            recipient="username123456"
        )
        expected = {
            'token': 'c26ef69d-5a7b-4186-9700-471aa0faea7d',
            'directmessage': {
                'entry': 'This is my entry,',
                'recipient': 'username123456',
                'timestamp': '1603167689.3928561'
            }
        }
        self.assertEqual(result, expected)

    def test_unread(self):
        '''This one tests for unread messages'''
        result = directmessage(
            token="c26ef69d-5a7b-4186-9700-471aa0faea7d",
            entry="new"
        )
        expected = {
            'token': 'c26ef69d-5a7b-4186-9700-471aa0faea7d',
            'directmessage': 'new'
        }
        self.assertEqual(result, expected)

    def test_allmessages(self):
        '''This tests for all messages'''
        result = directmessage(
            token="c26ef69d-5a7b-4186-9700-471aa0faea7d",
            entry="all"
        )
        expected = {
            'token': 'c26ef69d-5a7b-4186-9700-471aa0faea7d',
            'directmessage': 'all'
        }
        self.assertEqual(result, expected)

    def test_extract_json(self):
        '''This checks if function can convert json to namedtuple'''
        DataTuple = namedtuple('DataTuple',
                               ['response',
                                'type',
                                'message',
                                'messages'])
        test = json.dumps({
            "response": {
                "type": "ok",
                "messages": [
                    {"message":
                     "Hello User 1!",
                     "from": "markb",
                     "timestamp": "1603167689.3928561"},
                    {"message": "Bzzzzz",
                     "from": "thebeemoviescript",
                     "timestamp": "1603167689.3928561"}
                ]
            }
        })
        result = extract_json(test)
        expected = DataTuple(
            response={'type': 'ok', 'messages': [
                {'message': 'Hello User 1!',
                 'from': 'markb',
                 'timestamp': '1603167689.3928561'},
                {'message': 'Bzzzzz',
                 'from': 'thebeemoviescript',
                 'timestamp': '1603167689.3928561'}
            ]},
            type='ok',
            message=None,
            messages=[
                {'message': 'Hello User 1!',
                 'from': 'markb',
                 'timestamp': '1603167689.3928561'},
                {'message': 'Bzzzzz',
                 'from': 'thebeemoviescript',
                 'timestamp': '1603167689.3928561'}
            ]
        )
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
