# GitHub Sentinel
from subscription_manager import SubscriptionManager
from updater import Updater
from notifier import Notifier
from report_generator import ReportGenerator

class GitHubSentinel:
    def __init__(self):
        self.subscription_manager = SubscriptionManager()
        self.updater = Updater(self.subscription_manager)
        self.notifier = Notifier()
        self.report_generator = ReportGenerator()

    def run(self):
        subscriptions = self.subscription_manager.get_subscriptions()
        updates = self.updater.fetch_updates(subscriptions)
        self.notifier.send_notifications(updates)
        report = self.report_generator.generate_report(updates)
        return report

if __name__ == '__main__':
    sentinel = GitHubSentinel()
    report = sentinel.run()
    print(report)
