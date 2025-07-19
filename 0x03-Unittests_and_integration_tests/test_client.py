#!/usr/bin/env python3
"""
Unit and integration tests for the client module.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    # FIX IS HERE: Patch 'utils.get_json' directly at its source module.
    @patch('utils.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Tests that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument.
        """
        # Define the payload that our mocked get_json should return.
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        # Create an instance of GithubOrgClient with the parameterized org_name.
        client = GithubOrgClient(org_name)

        # Call the method under test.
        # This call will now correctly use the mocked get_json.
        result = client.org()

        # Assertion 1: Verify that the mocked get_json was called exactly once
        # with the correct GitHub API URL for the organization.
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assertion 2: Verify that the result returned by client.org()
        # matches our expected test_payload.
        self.assertEqual(result, test_payload)