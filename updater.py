# updater.py
import requests

class Updater:
    def __init__(self, subscription_manager):
        self.subscription_manager = subscription_manager

    def fetch_updates(self, subscriptions):
        updates = {}
        for repo_url in subscriptions:
            repo_name = repo_url.split('/')[-1]
            updates[repo_name] = self.get_repo_updates(repo_url)
        return updates

    def get_repo_updates(self, repo_url):
        response = requests.get(f'{repo_url}/commits')
        if response.status_code == 200:
            return response.json()
        return []
