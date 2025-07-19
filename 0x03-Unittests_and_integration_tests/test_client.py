#!/usr/bin/env python3
"""A module for testing the client module.
"""
import unittest
from typing import Dict
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import (
    GithubOrgClient
)
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""
    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch(
        "client.get_json",
    )
    def test_org(self, org: str, resp: Dict, mocked_fxn: MagicMock) -> None:
        """Tests the `org` method."""
        mocked_fxn.return_value = MagicMock(return_value=resp)
        gh_org_client = GithubOrgClient(org)
        self.assertEqual(gh_org_client.org(), resp)
        mocked_fxn.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )

    def test_public_repos_url(self) -> None:
        """Tests the `_public_repos_url` property."""
        with patch(
                "client.GithubOrgClient.org",
                new_callable=PropertyMock,
                ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method."""
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock,
                ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Tests the `has_license` method."""
        gh_org_client = GithubOrgClient("google")
        client_has_licence = gh_org_client.has_license(repo, key)
        self.assertEqual(client_has_licence, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()



@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class with mock patcher."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Return different payloads based on URL."""
            if "orgs/testorg" in url:
                return Mock(json=lambda: cls.org_payload)
            if "orgs/testorg/repos" in url:
                return Mock(json=lambda: cls.repos_payload)
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repositories."""
        client = GithubOrgClient("testorg")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter returns Apache-2.0 repos."""
        client = GithubOrgClient("testorg")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)



class TestGithubOrgClient(unittest.TestCase):
    """
    Tests the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('utils.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Tests that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument.
        """
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org()

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self) -> None:
        """
        Tests that _public_repos_url returns the correct URL based on
        a mocked org payload.
        """
        test_org_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock,
                   return_value=test_org_payload) as mock_org:

            client = GithubOrgClient("test")
            result = client._public_repos_url

            mock_org.assert_called_once()
            self.assertEqual(result, test_org_payload["repos_url"])

    @patch('utils.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Tests GithubOrgClient.public_repos returns the expected list of repos.
        Mocks both get_json and _public_repos_url.
        """
        test_repos_payload = [
            {"name": "alx-frontend", "license": {"key": "mit"}},
            {"name": "holberton-backend", "license": {"key": "apache-2.0"}},
            {"name": "project-x", "license": None},
        ]
        mock_get_json.return_value = test_repos_payload

        mock_repos_url = "https://api.github.com/users/test/repos"

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock,
                   return_value=mock_repos_url) as mock_public_repos_url:

            client = GithubOrgClient("test")
            result = client.public_repos()

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_repos_url)

            expected_repos = ["alx-frontend", "holberton-backend", "project-x"]
            self.assertEqual(result, expected_repos)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, license_key: str,
                         expected_result: bool) -> None:
        """
        Tests that GithubOrgClient.has_license returns the correct boolean value.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos using fixtures.
    """
    org_payload: dict
    repos_payload: list
    expected_repos: list
    apache2_repos: list

    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up the class-wide mocks for integration tests.
        Mocks requests.get to return appropriate payloads based on URL.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect_mock_get(url: str):
            """
            Side effect function for mock_get to return different payloads
            based on URL.
            """
            mock_response = MagicMock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]: # Use the actual repos_url from org_payload
                mock_response.json.return_value = cls.repos_payload
            else:
                # Handle unexpected URLs or raise an error
                raise requests.exceptions.RequestException(f"Unexpected URL: {url}")
            return mock_response

        cls.mock_get.side_effect = side_effect_mock_get

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Stops the patcher after all integration tests in the class are done.
        """
        cls.get_patcher.stop()

    def test_public_repos_integration(self) -> None:
        """
        Tests the public_repos method in an integration context
        without license filter.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)
        # Assert that requests.get was called twice: once for org, once for repos
        calls = [
            unittest.mock.call("https://api.github.com/orgs/google"),
            unittest.mock.call(self.org_payload["repos_url"]) # Use the actual repos_url
        ]
        self.mock_get.assert_has_calls(calls, any_order=True)

    def test_public_repos_with_license_integration(self) -> None:
        """
        Tests the public_repos method in an integration context
        with a license filter.
        """
        client = GithubOrgClient("google")
        # Ensure that the repos_payload has at least one repo with 'apache-2.0'
        # and one without, to properly test filtering.
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
        calls = [
            unittest.mock.call("https://api.github.com/orgs/google"),
            unittest.mock.call(self.org_payload["repos_url"]) # Use the actual repos_url
        ]
        self.mock_get.assert_has_calls(calls, any_order=True)



if __name__ == '__main__':
    unittest.main()











# #!/usr/bin/env python3
# """Unit tests for client.GithubOrgClient class."""

# import unittest
# from parameterized import parameterized
# from unittest.mock import patch, PropertyMock
# from client import GithubOrgClient


# class TestGithubOrgClient(unittest.TestCase):
#     """Test class for GithubOrgClient."""

#     @parameterized.expand([
#         ("google", {"login": "google", "id": 123456}),
#         ("abc", {"login": "abc", "id": 123456}),
#     ])
#     @patch('client.get_json')
#     def test_org(self, org_name, expected_response, mock_get_json):
#         """Test that GithubOrgClient.org returns correct value."""
#         mock_get_json.return_value = expected_response
#         client = GithubOrgClient(org_name)
#         result = client.org
#         expected_url = f"https://api.github.com/orgs/{org_name}"
#         mock_get_json.assert_called_once_with(expected_url)
#         self.assertEqual(result, expected_response)

#     def test_public_repos_url(self):
#         """Test that _public_repos_url returns correct URL."""
#         test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        
#         with patch('client.GithubOrgClient.org',
#                   new_callable=PropertyMock,
#                   return_value=test_payload) as mock_org:
#             client = GithubOrgClient("testorg")
#             result = client._public_repos_url
#             mock_org.assert_called_once()
#             self.assertEqual(result, test_payload["repos_url"])

#     @patch('client.get_json')
#     def test_public_repos(self, mock_get_json):
#         """Test that public_repos returns expected list of repos."""
#         test_repos = [
#             {"name": "repo1", "license": {"key": "mit"}},
#             {"name": "repo2", "license": {"key": "apache-2.0"}},
#         ]
#         test_url = "https://api.github.com/orgs/testorg/repos"
        
#         mock_get_json.return_value = test_repos
#         with patch('client.GithubOrgClient._public_repos_url',
#                   new_callable=PropertyMock,
#                   return_value=test_url) as mock_url:
#             client = GithubOrgClient("testorg")
#             result = client.public_repos()
#             mock_url.assert_called_once()
#             mock_get_json.assert_called_once_with(test_url)
#             expected_repos = ["repo1", "repo2"]
#             self.assertEqual(result, expected_repos)


# if __name__ == '__main__':
#     unittest.main()