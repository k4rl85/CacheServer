#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'carlo'

import unittest
import server
import time


ADDR_TEST = 'localhost'
PORT_TEST = 8080


class TestCacheServer(unittest.TestCase):
    def setUp(self):
        self.cache_server = server.CacheServer(ADDR_TEST, PORT_TEST, mode=server.TEST_MODE)

    def test_get_key_with_no_timer(self):
        """
        Test get_key method with a None value as timeout
        """
        test_key = 'key1'
        test_value = 'Monty Python'
        timeout = None
        self.cache_server.key_container[test_key] = [test_value, timeout]
        self.assertEqual(test_value, self.cache_server.get(test_key))

    def test_get_key_with_timeout_not_expired(self):
        """
        Test get_key method with a not expired timeout
        """
        test_key = 'key1'
        test_value = 'Monty Python'
        timeout = time.time() + 10
        self.cache_server.key_container[test_key] = [test_value, timeout]
        self.assertEqual(test_value, self.cache_server.get(test_key))

    def test_get_key_with_timeout_expired(self):
        """
        Test get_key method with a expired timeout
        """
        test_key = 'key1'
        test_value = 'Monty Python'
        timeout = time.time()
        self.cache_server.key_container[test_key] = [test_value, timeout]
        self.assertEqual(None, self.cache_server.get(test_key))

    def test_get_key_with_not_existent_key(self):
        """
        Test get_key method with unexistent key
        """
        test_key = 'unexistent_key'
        self.cache_server.key_container.pop(test_key, None)
        self.assertEqual(None, self.cache_server.get(test_key))

    def test_set_key_with_no_timeout_and_timeout_none(self):
        """
        Test set key with no timeout and timeout None
        """
        test_key = 'key1'
        test_value = 'Monty Python'

        self.assertIsNone(self.cache_server.set(test_key, test_value))
        self.assertEqual(test_value, self.cache_server.key_container[test_key][0])
        self.assertIsNone(self.cache_server.key_container[test_key][1])

    def test_set_key_with_timeout(self):
        """
        Test set key with no timeout and timeout None
        """
        test_key = 'key1'
        test_value = 'Monty Python'
        timeout = 10
        self.assertIsNone(self.cache_server.set(test_key, test_value, timeout))
        self.assertEqual(test_value, self.cache_server.key_container[test_key][0])
        self.assertIsInstance(self.cache_server.key_container[test_key][1], float)

    def test_delete_with_existent_key(self):
        """
        Test delete method with existent key
        """
        test_key = 'key1'
        test_value = 'Monty Python'
        timeout = 10
        self.cache_server.key_container[test_key] = [test_value, timeout]

        self.assertIn(test_key, self.cache_server.key_container)
        self.assertIsNone(self.cache_server.delete(test_key))
        self.assertNotIn(test_key, self.cache_server.key_container)

    def test_delete_with_not_existent_key(self):
        """
        Test delete method with not existent key
        """
        test_key = 'key1'
        self.cache_server.key_container.pop(test_key, None)

        self.assertNotIn(test_key, self.cache_server.key_container)
        self.assertIsNone(self.cache_server.delete(test_key))
        self.assertNotIn(test_key, self.cache_server.key_container)

    def test_set_many(self):
        """
        Test the set_many method with different type of value
        """
        key_to_be_injected = {'key1': 'Monty Python', 'key2': 353454, 'key3': True}

        for key in key_to_be_injected:
            self.assertNotIn(key, self.cache_server.key_container)

        self.cache_server.set_many(key_to_be_injected)

        for key in key_to_be_injected:
            self.assertIn(key, self.cache_server.key_container)

    def test_get_many_with_all_the_key_existent(self):
        """
        In this test all the value that i search are present in the server key_container
        """
        contained_key = {'key1': 'Monty Python', 'key2': 353454, 'key3': True}

        for key, value in contained_key.iteritems():
            self.cache_server.key_container[key] = [value, None]

        input_list = contained_key.keys()
        result_list = contained_key.values()

        self.assertEqual(result_list, self.cache_server.get_many(input_list))

        input_list.pop(1)
        result_list.pop(1)

        self.assertEqual(result_list, self.cache_server.get_many(input_list))

    def test_get_many_with_missing_key(self):
        """
        Test a get_many call with some key that doesn't exist in key_container
        """
        contained_key = {'key1': 'Monty Python', 'key2': 353454, 'key3': True}

        for key, value in contained_key.iteritems():
            self.cache_server.key_container[key] = [value, None]

        input_list = contained_key.keys()
        input_list.append('not_existent_key')
        result_list = contained_key.values()
        result_list.append(None)

        self.assertEqual(result_list, self.cache_server.get_many(input_list))

    def test_delete_many_with_all_key_existent(self):
        """
        Test a delete_many with all key present
        """
        contained_key = {'key1': 'Monty Python', 'key2': 353454, 'key3': True}

        for key, value in contained_key.iteritems():
            self.cache_server.key_container[key] = [value, None]

        input_list = contained_key.keys()
        self.cache_server.delete_many(input_list)
        self.assertEqual({}, self.cache_server.key_container)

    def test_incr_with_number_value(self):
        """
        This is the standard case with a key value incrementable
        """
        test_key = 'key1'
        test_value = 10
        self.cache_server.key_container[test_key] = [test_value, None]

        try:
            self.cache_server.incr(test_key)
            self.cache_server.incr(test_key, 3)
        except (TypeError, KeyError):
            # This assert must never happen
            self.assertTrue(False)

    def test_incr_with_key_value_not_numeric(self):
        """
        Test the case of incrementation a value not numeric
        """
        test_key = 'key1'
        test_value = '10'
        self.cache_server.key_container[test_key] = [test_value, None]

        self.assertRaises(ValueError, self.cache_server.incr, test_key)
        self.assertRaises(ValueError, self.cache_server.incr, test_key, 5)

    def test_incr_with_key_value_numeric_but_incremental_value_not_numeric(self):
        """
        Test the case of incrementation a value numeric but incremental value not numeric
        """
        test_key = 'key1'
        test_value = 10
        self.cache_server.key_container[test_key] = [test_value, None]

        self.assertRaises(ValueError, self.cache_server.incr, test_key, 'test')

    def test_incre_with_unexistent_key(self):
        """
        Test incr method with a unexistent key
        """
        test_key = 'key1'
        self.cache_server.key_container.pop(test_key, None)

        self.assertRaises(ValueError, self.cache_server.incr, test_key)
        self.assertRaises(ValueError, self.cache_server.incr, test_key, 5)
        self.assertRaises(ValueError, self.cache_server.incr, test_key, 'test')

    def test_decr_with_number_value(self):
        """
        This is the standard case with a key value decrementable
        """
        test_key = 'key1'
        test_value = 10
        self.cache_server.key_container[test_key] = [test_value, None]

        try:
            self.cache_server.decr(test_key)
            self.cache_server.decr(test_key, 3)
        except (TypeError, KeyError):
            # This assert must never happen
            self.assertTrue(False)

    def test_decr_with_key_value_not_numeric(self):
        """
        Test the case of decrementation a value not numeric
        """
        test_key = 'key1'
        test_value = '10'
        self.cache_server.key_container[test_key] = [test_value, None]

        self.assertRaises(ValueError, self.cache_server.decr, test_key)
        self.assertRaises(ValueError, self.cache_server.decr, test_key, 5)

    def test_decr_with_key_value_numeric_but_incremental_value_not_numeric(self):
        """
        Test the case of incrementation a value numeric but decremental value not numeric
        """
        test_key = 'key1'
        test_value = 10
        self.cache_server.key_container[test_key] = [test_value, None]

        self.assertRaises(ValueError, self.cache_server.decr, test_key, 'test')

    def test_decr_with_unexistent_key(self):
        """
        Test decr method with a unexistent key
        """
        test_key = 'key1'
        self.cache_server.key_container.pop(test_key, None)

        self.assertRaises(ValueError, self.cache_server.decr, test_key)
        self.assertRaises(ValueError, self.cache_server.decr, test_key, 5)
        self.assertRaises(ValueError, self.cache_server.decr, test_key, 'test')

    def test_get_and_set_together(self):
        """
        This test try a set and get in sequence
        """
        test_key = 'key1'
        test_value = 'Monty Python'
        self.cache_server.set(test_key, test_value)

        self.assertIn(test_key, self.cache_server.key_container)
        self.assertIn(test_value, self.cache_server.key_container[test_key])

        self.assertEqual(test_value, self.cache_server.get(test_key))

if __name__ == '__main__':
    unittest.main()
