# main.py
import gradio as gr
from datetime import datetime
from updater import GitHubClient
from report_generator import ReportGenerator
from llm import LLM

# 初始化各个模块
github_client = GitHubClient()
llm = LLM()
report_generator = ReportGenerator(llm)


# 定义生成每日进展的函数
def generate_progress(repo_url):
    try:
        print(f"正在生成 {repo_url} 的每日进展...")
        print(github_client)
        github_client.export_progress_to_markdown(repo_url)
        return f"进展文件生成成功：{repo_url.split('/')[-1]}_{datetime.now().strftime('%Y-%m-%d')}.md"
    except Exception as e:
        return f"生成进展文件失败: {e}"


# 定义生成每日报告的函数
def generate_report(repo_name):
    try:
        date_str = datetime.now().strftime("%Y-%m-%d")
        report_generator.generate_daily_report(repo_name, date_str)
        return f"每日项目报告生成成功：{repo_name}_daily_report_{date_str}.md"
    except Exception as e:
        return f"生成每日项目报告失败: {e}"


# 定义 Gradio 界面
with gr.Blocks() as gui:
    gr.Markdown("# GitHub Sentinel - 项目管理工具")

    with gr.Tab("生成每日进展"):
        repo_url_input = gr.Textbox(label="GitHub 仓库 URL",
                                    placeholder="例如：https://github.com/langchain-ai/langchain")
        progress_button = gr.Button("生成每日进展")
        progress_output = gr.Textbox(label="输出")

        # 绑定按钮与函数
        progress_button.click(fn=generate_progress, inputs=repo_url_input, outputs=progress_output)

    with gr.Tab("生成每日报告"):
        repo_name_input = gr.Textbox(label="仓库名称", placeholder="例如：langchain")
        report_button = gr.Button("生成每日报告")
        report_output = gr.Textbox(label="输出")

        # 绑定按钮与函数
        report_button.click(fn=generate_report, inputs=repo_name_input, outputs=report_output)

    # 显示退出按钮
    quit_button = gr.Button("退出")
    quit_button.click(lambda: "应用已退出", None, None)

# 运行 Gradio 应用
if __name__ == "__main__":
    gui.launch(share=True)