import unittest
from unittest.mock import patch

from jk.GitHubSentinel.scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.repos = ["https://github.com/test/repo1"]
        self.scheduler = Scheduler(self.repos, "test_token", "test_key")

    @patch('updater.GitHubClient.export_progress_to_markdown')
    @patch('report_generator.ReportGenerator.generate_daily_report')
    def test_generate_daily_progress_and_report(self, mock_generate_report, mock_export_progress):
        """测试生成每日进展和报告"""
        self.scheduler.generate_daily_progress_and_report()

        mock_export_progress.assert_called_once()
        mock_generate_report.assert_called_once()