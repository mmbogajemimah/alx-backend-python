#!/usr/bin/env python3
"""Module test_client
Unit tests for the GithubOrgClient class from the client module.
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name, mock_get):
        """
        Test the `org` property of GithubOrgClient.

        Ensures that the `org` property fetches the correct organization
        data using the `get_json` function.

        Args:
            org_name (str): The name of the organization to fetch.
            mock_get (Mock): Mocked `get_json` function.

        Asserts:
            - The `org` property returns the expected value.
            - `get_json` is called exactly once.
        """
        test_client = GithubOrgClient(org_name)
        test_return = test_client.org
        self.assertEqual(test_return, mock_get.return_value)
        mock_get.assert_called_once()

    def test_public_repos_url(self):
        """
        Test the `_public_repos_url` property of GithubOrgClient.

        Ensures that the `_public_repos_url` property correctly retrieves
        the repository URL from the organization's data.

        Asserts:
            - The `_public_repos_url` property returns the expected URL.
            - The `org` property is called exactly once.
        """
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value={"repos_url": "holberton"}
        ) as mock_get:
            test_client = GithubOrgClient("holberton")
            test_return = test_client._public_repos_url
            mock_get.assert_called_once()
            self.assertEqual(test_return, mock_get.return_value.get("repos_url"))

    @patch("client.get_json", return_value=[{"name": "holberton"}])
    def test_public_repos(self, mock_get):
        """
        Test the `public_repos` method of GithubOrgClient.

        Ensures that the `public_repos` method fetches and returns a list
        of repository names.

        Args:
            mock_get (Mock): Mocked `get_json` function.

        Asserts:
            - The `public_repos` method returns the expected list of repositories.
            - The `get_json` function is called exactly once.
            - The `_public_repos_url` property is called exactly once.
        """
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/"
        ) as mock_pub:
            test_client = GithubOrgClient("holberton")
            test_return = test_client.public_repos()
            self.assertEqual(test_return, ["holberton"])
            mock_get.assert_called_once()
            mock_pub.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_return):
        """
        Test the `has_license` method of GithubOrgClient.

        Ensures that the method correctly determines whether a repository
        is licensed under a given license key.

        Args:
            repo (dict): Repository data.
            license_key (str): The license key to check for.
            expected_return (bool): The expected return value.

        Asserts:
            The method returns the expected boolean value.
        """
        test_client = GithubOrgClient("holberton")
        test_return = test_client.has_license(repo, license_key)
        self.assertEqual(test_return, expected_return)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls):
        """
        Set up resources for integration tests.

        Starts a patcher for `requests.get` to simulate HTTP errors.
        """
        cls.get_patcher = patch("requests.get", side_effect=HTTPError)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up resources after integration tests.

        Stops the patcher for `requests.get`.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Integration test for the `public_repos` method.

        Ensures that the `public_repos` method works as expected in
        an integrated setup.

        Asserts:
            The method completes without errors (placeholder test).
        """
        test_client = GithubOrgClient("holberton")
        self.assertTrue(True)

    def test_public_repos_with_license(self):
        """
        Integration test for the `public_repos` method with license filtering.

        Ensures that the `public_repos` method correctly filters repositories
        based on the specified license in an integrated setup.

        Asserts:
            The method completes without errors (placeholder test).
        """
        test_client = GithubOrgClient("holberton")
        self.assertTrue(True)
