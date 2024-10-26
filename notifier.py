# notifier.py
class Notifier:
    def send_notifications(self, updates):
        for repo, commits in updates.items():
            print(f'Repo: {repo}, New commits: {len(commits)}')
