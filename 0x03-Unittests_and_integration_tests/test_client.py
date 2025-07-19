#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient class."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google", {"login": "google", "id": 123456}),
        ("abc", {"login": "abc", "id": 123456}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test that GithubOrgClient.org returns correct value."""
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        result = client.org
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_response)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL."""
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        
        with patch('client.GithubOrgClient.org',
                  new_callable=PropertyMock,
                  return_value=test_payload) as mock_org:
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            mock_org.assert_called_once()
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repos."""
        test_repos = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        test_url = "https://api.github.com/orgs/testorg/repos"
        
        mock_get_json.return_value = test_repos
        with patch('client.GithubOrgClient._public_repos_url',
                  new_callable=PropertyMock,
                  return_value=test_url) as mock_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)
            expected_repos = ["repo1", "repo2"]
            self.assertEqual(result, expected_repos)


if __name__ == '__main__':
    unittest.main()