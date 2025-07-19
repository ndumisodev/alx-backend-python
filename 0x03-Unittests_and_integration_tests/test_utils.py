#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
import requests

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests the access_nested_map function from utils.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict,
                               path: tuple, expected_result: any) -> None:
        """
        Tests that access_nested_map returns the expected result for valid inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map: dict,
                                         path: tuple, expected_key: str) -> None:
        """
        Tests that access_nested_map raises a KeyError with the expected message
        for invalid paths.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """
    Tests the get_json function from utils.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: dict,
                       mock_requests_get: Mock) -> None:
        """
        Tests that get_json returns the expected result by mocking requests.get.
        """
        # Configure the mock object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_requests_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assertions
        mock_requests_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


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



# #!/usr/bin/env python3
# """ Unit tests for utils.access_nested_map function """
# import unittest
# from parameterized import parameterized
# from utils import access_nested_map
# from unittest.mock import patch, Mock
# from utils import get_json
# from unittest.mock import patch
# from utils import memoize

# class TestAccessNestedMap(unittest.TestCase):
#     """ Test class for access_nested_map """
    
#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2),
#     ])
#     def test_access_nested_map(self, nested_map, path, expected):
#         """ Test access_nested_map returns correct value """
#         self.assertEqual(access_nested_map(nested_map, path), expected)


# #!/usr/bin/env python3
# """ Unit tests for utils.access_nested_map function """

# class TestAccessNestedMap(unittest.TestCase):
#     """ Test class for access_nested_map """
    
#     # Previous test cases for successful access
#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2),
#     ])
#     def test_access_nested_map(self, nested_map, path, expected):
#         """ Test access_nested_map returns correct value """
#         self.assertEqual(access_nested_map(nested_map, path), expected)

#     # New test cases for exception handling
#     @parameterized.expand([
#         ({}, ("a",), "'a'"),
#         ({"a": 1}, ("a", "b"), "'b'"),
#     ])
#     def test_access_nested_map_exception(self, nested_map, path, expected_msg):
#         """ Test access_nested_map raises KeyError with expected message """
#         with self.assertRaises(KeyError) as context:
#             access_nested_map(nested_map, path)
#         self.assertEqual(str(context.exception), expected_msg)



# class TestGetJson(unittest.TestCase):
#     """ Test class for get_json function """
    
#     @parameterized.expand([
#         ("http://example.com", {"payload": True}),
#         ("http://holberton.io", {"payload": False}),
#     ])
#     def test_get_json(self, test_url, test_payload):
#         """ Test get_json returns the expected result without making actual HTTP calls """
#         # Create a mock response object
#         mock_response = Mock()
#         mock_response.json.return_value = test_payload
        
#         # Patch requests.get to return our mock response
#         with patch('requests.get', return_value=mock_response) as mock_get:
#             # Call the function
#             result = get_json(test_url)
            
#             # Assert the mock was called exactly once with test_url
#             mock_get.assert_called_once_with(test_url)
            
#             # Assert the result matches test_payload
#             self.assertEqual(result, test_payload)



# class TestMemoize(unittest.TestCase):
#     """
#     Tests the memoize decorator from utils.
#     """

#     def test_memoize(self) -> None:
#         """
#         Tests that a method decorated with memoize is called only once.
#         """
#         class TestClass:
#             """A test class for memoization."""
#             def a_method(self) -> int:
#                 """Returns a fixed value."""
#                 return 42

#             @memoize
#             def a_property(self) -> int:
#                 """A memoized property that calls a_method."""
#                 return self.a_method()

#         with patch.object(TestClass, 'a_method',
#                           return_value=42) as mock_a_method:
#             test_instance = TestClass()

#             # Call the memoized property twice
#             result1 = test_instance.a_property
#             result2 = test_instance.a_property

#             # Assertions
#             self.assertEqual(result1, 42)
#             self.assertEqual(result2, 42)
#             mock_a_method.assert_called_once()




