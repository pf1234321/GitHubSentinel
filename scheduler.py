# scheduler.py
import schedule
import time
from datetime import datetime
from updater import GitHubClient
from report_generator import ReportGenerator
from llm import LLM


class Scheduler:
    def __init__(self, repos, github_token=None, openai_key=None):
        self.repos = repos  # 订阅的项目列表，格式为 GitHub 仓库 URL 列表
        self.github_client = GitHubClient(github_token)
        self.llm = LLM(api_key=openai_key)
        self.report_generator = ReportGenerator(self.llm)

    def generate_daily_progress_and_report(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        for repo_url in self.repos:
            print(f"Processing {repo_url} for {date_str}...")
            repo_name = repo_url.split('/')[-1]

            # 生成每日进展文件
            self.github_client.export_progress_to_markdown(repo_url)

            # 生成每日报告文件
            self.report_generator.generate_daily_report(repo_name, date_str)

    def schedule_daily_task(self, hour=9, minute=0):
        # 每天在指定时间运行任务
        schedule.every().day.at(f"{hour:02}:{minute:02}").do(self.generate_daily_progress_and_report)
        print(f"每日定时任务已设定：每天 {hour:02}:{minute:02} 执行")

        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次任务
