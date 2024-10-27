# updater.py
import requests
import os
from datetime import datetime


class GitHubClient:
    def __init__(self, github_token=None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.headers = {"Authorization": f"token {self.github_token}"} if self.github_token else {}

    def fetch_issues(self, repo_url):
        api_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/issues"
        response = requests.get(api_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def fetch_pull_requests(self, repo_url):
        api_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/pulls"
        response = requests.get(api_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def export_progress_to_markdown(self, repo_url):
        repo_name = repo_url.split('/')[-1]
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{repo_name}_{date_str}.md"

        issues = self.fetch_issues(repo_url)
        pulls = self.fetch_pull_requests(repo_url)

        with open(filename, "w") as file:
            file.write(f"# {repo_name} Daily Progress - {date_str}\n\n")
            file.write("## Issues\n")
            for issue in issues:
                file.write(f"- [{issue['title']}]({issue['html_url']})\n")

            file.write("\n## Pull Requests\n")
            for pr in pulls:
                file.write(f"- [{pr['title']}]({pr['html_url']})\n")

        print(f"进展文件已生成：{filename}")
