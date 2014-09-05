#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'carlo'

import time
from SimpleXMLRPCServer import SimpleXMLRPCServer

# In case of test we must put on False bind_and_activate on SimpleXMLRPCServer
TEST_MODE = False
NORMAL_USE = True


class CacheServer(object):
    def __init__(self, addr='localhost', port=8080, mode=NORMAL_USE):
        self.key_container = {}
        self.server_state = True
        self.server = SimpleXMLRPCServer((addr, port), allow_none=True, bind_and_activate=mode)
        self.server.register_function(self.set)
        self.server.register_function(self.get)
        self.server.register_function(self.delete)
        self.server.register_function(self.set_many)
        self.server.register_function(self.get_many)
        self.server.register_function(self.delete_many)
        self.server.register_function(self.incr)
        self.server.register_function(self.decr)
        self.server.register_function(self.quit)

    def get(self, key):
        """
        Get method that search a key in self.key_container.
        If the key is present and not expired the relative value is returned
        :param key: The searched key
        :return: The value relative of key if the key is present and not expired
        """
        if key in self.key_container:
            searched = self.key_container[key]
            if searched[1] is not None and searched[1] <= time.time():
                self.key_container.pop(key, None)
                return None
            else:
                return searched[0]
        return None

    def set(self, key, value, timeout=None):
        """
        Allow to set a key with a value and optional timeout
        :param key: The name of key to be entered
        :param value: the value relative the entered key
        :param timeout: Optional timeout of value entered
        """
        if timeout is not None:
            time_key = time.time() + timeout
        else:
            time_key = None
        self.key_container[key] = [value, time_key]

    def delete(self, key):
        """
        Delete the key entered if it exist
        :param key: The name of the key deleted
        """
        try:
            self.key_container.pop(key)
        except KeyError:
            pass

    def set_many(self, received_keys):
        """
        Allow to set of many key
        :param received_keys: A dictionary contain key and relative value
        """
        for key, value in received_keys.iteritems():
            self.set(key, value)

    def get_many(self, searched_list):
        """
        Receive an array of searched key and return an array with the relative key if they are present.
        If some/all key are missing the result array contain None in the same spot of missing key.
        :param searched_list: Array containing searched keys
        :return: Array with value relative of entered keys
        """
        response = []
        for key in searched_list:
            if key in self.key_container:
                response.append(self.get(key))
            else:
                response.append(None)
        return response

    def delete_many(self, delete_list):
        """
        Receive an array of key and delete all relative value if present.
        :param delete_list: A list of key to be deleted
        """
        for key in delete_list:
            self.delete(key)

    def incr(self, key, val=1):
        """
        Increment the value relative key by the same value received in val, default 1.
        if the key is not present, or the relative value is not a number or the received val is not a number
        raise ValueError.
        :param key: The key incremented
        :param val: The value incremented
        """
        try:
            self.key_container[key][0] += val
        except (TypeError, KeyError, ValueError):
            raise ValueError

    def decr(self, key, val=1):
        """
        Decrement the value relative key by the same value received in val, default 1.
        if the key is not present, or the relative value is not a number or the received val is not a number
        raise ValueError.
        :param key: The key decremented
        :param val: The value decremented
        """
        try:
            self.key_container[key][0] -= val
        except (TypeError, KeyError, ValueError):
            raise ValueError

    def quit(self):
        self.server_state = False

    def start_server(self):
        try:
            while self.server_state:
                self.server.handle_request()
                print '\nKey_container contain:', self.key_container, '\n'
        except KeyboardInterrupt:
            pass


def main():
    server = CacheServer()
    server.start_server()

if __name__ == '__main__':
    main()
