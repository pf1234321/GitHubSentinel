import unittest
from unittest.mock import patch

from jk.GitHubSentinel.report_generator import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.report_generator = ReportGenerator()
        self.test_sources = [
            {
                "type": "GitHub",
                "url": "https://github.com/test/repo1",
                "keywords": ["test", "demo"],
                "data": {"issues": 5, "alerts": 2}
            }
        ]

    def test_generate_summary_report(self):
        """测试生成摘要报告"""
        result = self.report_generator.generate_summary_report(self.test_sources)

        self.assertEqual(result["status"], "success")
        self.assertIn("content", result)
        self.assertIn("paths", result)
        self.assertIn("metadata", result)

    def test_generate_detailed_report(self):
        """测试生成详细报告"""
        result = self.report_generator.generate_detailed_report(self.test_sources)

        self.assertEqual(result["status"], "success")
        self.assertIn("content", result)
        self.assertIn("paths", result)

    def test_generate_alert_report(self):
        """测试生成警报报告"""
        result = self.report_generator.generate_alert_report(self.test_sources)

        self.assertEqual(result["status"], "success")
        self.assertIn("content", result)
        self.assertIn("paths", result)

    def test_error_handling(self):
        """测试错误处理"""
        with patch('report_generator.summarize_progress', side_effect=Exception("Test error")):
            result = self.report_generator.generate_summary_report([])
            self.assertEqual(result["status"], "error")
            self.assertIn("error", result)