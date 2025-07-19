#!/usr/bin/env python3
""" Unit tests for utils.access_nested_map function """
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json
from unittest.mock import patch
from utils import memoize

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



# class TestMemoize(unittest.TestCase):
#     """ Test class for memoize decorator """
    
#     def test_memoize(self):
#         """ Test that memoize caches the result properly """
        
#         class TestClass:
#             """ Test class with memoized property """
            
#             def a_method(self):
#                 return 42

#             @memoize
#             def a_property(self):
#                 return self.a_method()
        
#         # Create instance of test class
#         test_instance = TestClass()
        
#         # Patch a_method to track calls and return 42
#         with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
#             # First call to a_property
#             result1 = test_instance.a_property()
#             # Second call to a_property
#             result2 = test_instance.a_property()
            
#             # Assert correct results
#             self.assertEqual(result1, 42)
#             self.assertEqual(result2, 42)
            
#             # Assert a_method was called only once
#             mock_method.assert_called_once()


# class TestMemoize(unittest.TestCase):
#     """Test for memoize decorator"""

#     def test_memoize(self):
#         """Test that a_method is only called once due to memoization"""

#         class TestClass:
#             def a_method(self):
#                 return 42

#             @memoize
#             def a_property(self):
#                 return self.a_method()

#         with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
#             test_obj = TestClass()

#             result1 = test_obj.a_property
#             result2 = test_obj.a_property

#             self.assertEqual(result1, 42)
#             self.assertEqual(result2, 42)
#             mock_method.assert_called_once()



class TestMemoize(unittest.TestCase):
    """
    Tests the memoize decorator from utils.
    """

    def test_memoize(self) -> None:
        """
        Tests that a method decorated with memoize is called only once.
        """
        class TestClass:
            """A test class for memoization."""
            def a_method(self) -> int:
                """Returns a fixed value."""
                return 42

            @memoize
            def a_property(self) -> int:
                """A memoized property that calls a_method."""
                return self.a_method()

        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_a_method:
            test_instance = TestClass()

            # Call the memoized property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assertions
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()


