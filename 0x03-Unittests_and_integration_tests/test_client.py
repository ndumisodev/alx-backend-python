#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient class."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        without making external HTTP calls.
        """
        # Set up the mock return value
        test_payload = {"login": org_name, "id": 123456}
        mock_get_json.return_value = test_payload

        # Create client instance and call the method
        client = GithubOrgClient(org_name)
        result = client.org

        # Verify get_json was called exactly once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Verify the result matches the mock return value
        self.assertEqual(result, test_payload)