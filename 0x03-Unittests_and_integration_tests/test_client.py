#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient class."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    # Task 4: Parameterize and patch as decorators
    @parameterized.expand([
        ("google", {"login": "google", "id": 123456}),
        ("abc", {"login": "abc", "id": 123456}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, mock_get_json):
        """
        Test that GithubOrgClient.org returns correct value.
        Mock get_json to avoid external HTTP calls.
        """
        # Configure mock to return our expected response
        mock_get_json.return_value = expected_response

        # Create client and call org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Verify get_json was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Verify result matches expected response
        self.assertEqual(result, expected_response)

    # Task 5: Mocking a property
    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL."""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }
        
        # Patch org property to return our test payload
        with patch('client.GithubOrgClient.org',
                 new_callable=PropertyMock,
                 return_value=test_payload) as mock_org:
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            
            # Verify org property was accessed
            mock_org.assert_called_once()
            
            # Verify correct URL is returned
            self.assertEqual(result, test_payload["repos_url"])

    # Task 6: More patching
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repos."""
        # Test data
        test_repos = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        test_url = "https://api.github.com/orgs/testorg/repos"
        
        # Configure mocks
        mock_get_json.return_value = test_repos
        with patch('client.GithubOrgClient._public_repos_url',
                  new_callable=PropertyMock,
                  return_value=test_url) as mock_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()
            
            # Verify mocks were called
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)
            
            # Verify we get just the repo names
            expected_repos = ["repo1", "repo2"]
            self.assertEqual(result, expected_repos)