# report_generator.py
from llm import LLM
from datetime import datetime


class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_daily_report(self, repo_name, date_str):
        filename = f"{repo_name}_{date_str}.md"
        with open(filename, "r") as file:
            content = file.read()

        summary = self.llm.summarize_progress(content)

        report_filename = f"{repo_name}_daily_report_{date_str}.md"
        with open(report_filename, "w") as report_file:
            report_file.write(f"# {repo_name} Daily Report - {date_str}\n\n")
            report_file.write(summary)

        print(f"每日项目报告已生成：{report_filename}")
