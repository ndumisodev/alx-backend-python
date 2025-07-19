#!/usr/bin/env python3
""" Unit tests for utils.access_nested_map function """
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json

class TestAccessNestedMap(unittest.TestCase):
    """ Test class for access_nested_map """
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test access_nested_map returns correct value """
        self.assertEqual(access_nested_map(nested_map, path), expected)


#!/usr/bin/env python3
""" Unit tests for utils.access_nested_map function """

class TestAccessNestedMap(unittest.TestCase):
    """ Test class for access_nested_map """
    
    # Previous test cases for successful access
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test access_nested_map returns correct value """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # New test cases for exception handling
    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_msg):
        """ Test access_nested_map raises KeyError with expected message """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_msg)



class TestGetJson(unittest.TestCase):
    """ Test class for get_json function """
    
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """ Test get_json returns the expected result without making actual HTTP calls """
        # Create a mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        
        # Patch requests.get to return our mock response
        with patch('requests.get', return_value=mock_response) as mock_get:
            # Call the function
            result = get_json(test_url)
            
            # Assert the mock was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)
            
            # Assert the result matches test_payload
            self.assertEqual(result, test_payload)