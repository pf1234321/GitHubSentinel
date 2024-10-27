# main.py
from updater import GitHubClient
from report_generator import ReportGenerator
from llm import LLM
from datetime import datetime


def main():
    github_client = GitHubClient()
    llm = LLM()
    report_generator = ReportGenerator(llm)

    while True:
        command = input("请输入命令（progress、report、quit）：")

        if command == "progress":
            repo_url = input("请输入仓库 URL：")
            github_client.export_progress_to_markdown(repo_url)

        elif command == "report":
            repo_name = input("请输入仓库名称：")
            date_str = datetime.now().strftime("%Y-%m-%d")
            report_generator.generate_daily_report(repo_name, date_str)

        elif command == "quit":
            print("退出 GitHub Sentinel...")
            break

        else:
            print("未知命令。请输入 'progress'、'report' 或 'quit'。")


if __name__ == "__main__":
    main()
