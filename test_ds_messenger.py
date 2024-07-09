'''This file tests ds_messenger functions'''
import unittest
from ds_messenger import DirectMessenger, DirectMessage


class TestDirectMessenger(unittest.TestCase):
    '''This class holds the tests for ds_messenger'''

    def test_send_message(self):
        '''This will test send_message'''
        dm = DirectMessenger(dsuserver='168.235.86.101',
                             username='user',
                             password='pass')
        result = dm.send_message('Does this work', 'katpham')
        self.assertTrue(result)

    def test_retrieve_new(self):
        '''This tests retrieve_new'''
        dm = DirectMessenger(dsuserver='168.235.86.101',
                             username='user',
                             password='pass')
        result = dm.retrieve_new()
        self.assertIsInstance(result, list)
        for message in result:
            self.assertIsInstance(message, DirectMessage)

    def test_retrieve_all(self):
        '''This tests retrieve_all'''
        dm = DirectMessenger(dsuserver='168.235.86.101',
                             username='user',
                             password='pass')
        result = dm.retrieve_all()
        self.assertIsInstance(result, list)
        for message in result:
            self.assertIsInstance(message, DirectMessage)


if __name__ == '__main__':
    unittest.main()
