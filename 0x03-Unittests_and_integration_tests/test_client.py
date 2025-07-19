#!/usr/bin/env python3
"""
Unit and integration tests for the client module.
"""
import unittest
# Import patch and Mock directly from unittest.mock
from unittest.mock import patch, Mock
from parameterized import parameterized

from client import GithubOrgClient # Import the class to be tested


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    # IMPORTANT CHANGE: Removed the @patch decorator here.
    # We will use patch as a context manager inside the method.
    def test_org(self, org_name: str) -> None:
        """
        Tests that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument.
        """
        test_payload = {"login": org_name}
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # FIX IS HERE: Use patch as a context manager inside the test method.
        # Patch 'utils.get_json' as it's the original source of the function.
        # This ensures the mock is active precisely when client.org() calls it.
        with patch('utils.get_json') as mock_get_json:
            # Configure the mock object that replaces utils.get_json
            mock_get_json.return_value = test_payload

            # Create an instance of GithubOrgClient with the parameterized org_name.
            client = GithubOrgClient(org_name)

            # Call the method under test.
            # This call will now correctly use the mocked get_json.
            result = client.org()

            # Assertion 1: Verify that the mocked get_json was called exactly once
            # with the correct GitHub API URL for the organization.
            mock_get_json.assert_called_once_with(expected_url)

            # Assertion 2: Verify that the result returned by client.org()
            # matches our expected test_payload.
            self.assertEqual(result, test_payload)