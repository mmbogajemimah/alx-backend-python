#!/usr/bin/env python3
"""Unit tests for utility functions in the utils module.
"""

import unittest
from typing import Mapping, Any, Sequence
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self,
                               nested_map: Mapping[str, Any],
                               path: Sequence[str],
                               expected: Any) -> None:
        """
        Verify that access_nested_map retrieves the correct value.

        Args:
            nested_map (Mapping): A dictionary with nested data.
            path (Sequence): A sequence of keys to navigate the map.
            expected (Any): The expected value for the given path.

        Asserts:
            The function returns the expected value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Mapping[str, Any],
                                         path: Sequence[str]) -> None:
        """
        Verify that access_nested_map raises KeyError for invalid paths.

        Args:
            nested_map (Mapping): A dictionary with nested data.
            path (Sequence): A sequence of keys to navigate the map.

        Asserts:
            The function raises a KeyError if the path is invalid.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """
        Verify that get_json fetches and returns the correct JSON response.

        Args:
            test_url (str): The URL to fetch JSON data from.
            test_payload (dict): The expected JSON payload.

        Asserts:
            The function returns the expected JSON data.
        """
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""
    def test_memoize(self):
        """
        Verify that the memoize decorator caches method results.

        Ensures that a method decorated with @memoize is only called
        once, even when accessed multiple times.
        """
        class TestClass:
            """Helper class to test the memoize decorator."""
            def a_method(self):
                """Simulate a method that returns a fixed value."""
                return 42

            @memoize
            def a_property(self):
                """A memoized method that returns the value of a_method."""
                return self.a_method()

        with patch.object(TestClass, "a_method") as mockMethod:
            test_class = TestClass()
            test_class.a_property  
            test_class.a_property  
            mockMethod.assert_called_once()


if __name__ == '__main__':
    unittest.main()
