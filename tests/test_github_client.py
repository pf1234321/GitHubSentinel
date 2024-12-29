import unittest
from unittest.mock import patch, Mock

from jk.GitHubSentinel.updater import GitHubClient


class TestGitHubClient(unittest.TestCase):
    def setUp(self):
        self.client = GitHubClient("test_token")
        self.test_repo = "test/repo"

    @patch('requests.get')
    def test_fetch_issues(self, mock_get):
        """测试获取 Issues"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"title": "Test Issue"}]
        mock_get.return_value = mock_response

        issues = self.client.fetch_issues(f"https://github.com/{self.test_repo}")
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["title"], "Test Issue")

    @patch('requests.get')
    def test_fetch_pull_requests(self, mock_get):
        """测试获取 Pull Requests"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"title": "Test PR"}]
        mock_get.return_value = mock_response

        prs = self.client.fetch_pull_requests(f"https://github.com/{self.test_repo}")
        self.assertEqual(len(prs), 1)
        self.assertEqual(prs[0]["title"], "Test PR")

    @patch('requests.get')
    def test_fetch_commits(self, mock_get):
        """测试获取 Commits"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"commit": {"message": "Test Commit"}}]
        mock_get.return_value = mock_response

        commits = self.client.fetch_commits(f"https://github.com/{self.test_repo}")
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0]["commit"]["message"], "Test Commit")