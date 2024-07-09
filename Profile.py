'''This file stores Profile and Post content'''
# Profile.py
#
# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON
# SERIALIZATION ASPECTS OF THIS CODE
# RIGHT NOW, though can you certainly take a look at it
# if you are curious since we
# already covered a bit of the JSON format in class.
#
import json
import time
from pathlib import Path


class DsuFileError(Exception):
    '''Exception for DsuFileError'''
    pass


class DsuProfileError(Exception):
    '''Exception for ProfileError'''
    pass


class Post(dict):
    """
    Class that stores Post functionalities & variables
    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        '''init Post variables'''
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        '''Lets you set an entry'''
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        '''returns the entry'''
        return self._entry

    def set_time(self, time: float):
        '''sets the time'''
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        '''gets the time'''
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    Profile holds content for a user profile
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        '''initializes these variables'''
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ''
        self._posts = []

        self.friends = []
        self.messages = []

    def add_post(self, post: Post) -> None:
        '''adds a post to the posts list'''
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        '''Deletes a post in list by index'''
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        '''Returns list of posts'''
        return self._posts

    def save_profile(self, path: str) -> None:
        '''Saves profile'''
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError(
                    "Error while attempting to process the DSU file.", ex
                    )
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def add_friend(self, friend):
        '''appends a friend to friends list'''
        self.friends.append(friend)

    def get_friend(self):
        '''returns friends list'''
        return self.friends

    def add_message(self, message):
        '''appends a message to messages list'''
        self.messages.append(message)

    def get_message(self):
        '''returns the friends list'''
        return self.messages

    def load_profile(self, path: str) -> None:
        '''load_profile will populate the current instance of
        Profile with data stored in a
        DSU file.'''

        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)

                for friend in self.friends:
                    if friend not in self.friends:
                        self.add_friend(friend)
                for message in self.messages:
                    if message not in self.messages:
                        self.add_message(message)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
