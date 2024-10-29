import os


class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_daily_report(self, repo_name, date_str):
        # 获取当前脚本所在的目录
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 将文件路径设置为该目录下的文件
        filename = os.path.join(base_dir, f"{repo_name}_{date_str}.md")
        report_filename = os.path.join(base_dir, f"{repo_name}_daily_report_{date_str}.md")
        if not os.path.exists(filename):
            print(f"文件 {filename} 不存在")
            return
        try:
            with open(filename, "r") as file:
                content = file.read()

            summary = self.llm.summarize_progress(content)

            with open(report_filename, "w") as report_file:
                report_file.write(f"# {repo_name} Daily Report - {date_str}\n\n")
                report_file.write(summary)

            print(f"每日项目报告已生成：{report_filename}")
        except FileNotFoundError:
            print(f"文件 {filename} 未找到，请检查文件路径。")
