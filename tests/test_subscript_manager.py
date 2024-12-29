import unittest
import json
import os

from jk.GitHubSentinel.subscription_manager import SubscriptionManager


class TestSubscriptionManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_subscriptions.json"
        self.manager = SubscriptionManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_subscription(self):
        """测试添加订阅"""
        test_url = "https://github.com/test/repo"
        self.manager.add_subscription(test_url)

        self.assertIn(test_url, self.manager.get_subscriptions())

    def test_remove_subscription(self):
        """测试移除订阅"""
        test_url = "https://github.com/test/repo"
        self.manager.add_subscription(test_url)
        self.manager.remove_subscription(test_url)

        self.assertNotIn(test_url, self.manager.get_subscriptions())

    def test_load_subscriptions(self):
        """测试加载订阅"""
        test_urls = ["https://github.com/test/repo1", "https://github.com/test/repo2"]
        with open(self.test_file, 'w') as f:
            json.dump(test_urls, f)

        self.manager.load_subscriptions()
        self.assertEqual(self.manager.get_subscriptions(), test_urls)