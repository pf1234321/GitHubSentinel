# subscription_manager.py
import json

class SubscriptionManager:
    def __init__(self, subscription_file='subscriptions.json'):
        self.subscription_file = subscription_file
        self.load_subscriptions()

    def load_subscriptions(self):
        try:
            with open(self.subscription_file, 'r') as file:
                self.subscriptions = json.load(file)
        except FileNotFoundError:
            self.subscriptions = []

    def save_subscriptions(self):
        with open(self.subscription_file, 'w') as file:
            json.dump(self.subscriptions, file)

    def add_subscription(self, repo_url):
        self.subscriptions.append(repo_url)
        self.save_subscriptions()

    def remove_subscription(self, repo_url):
        self.subscriptions.remove(repo_url)
        self.save_subscriptions()

    def get_subscriptions(self):
        return self.subscriptions
