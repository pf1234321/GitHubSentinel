import os
import openai
import configparser

class LLM:
    def __init__(self):
        # 加载配置文件
        config = configparser.ConfigParser()
        config.read("config.ini")

        # 从配置文件中获取 api_key 和 api_base
        openai.api_key = config.get("openai", "api_key")
        openai.api_base = config.get("openai", "api_base")

    def summarize_progress(self, content):
        chat_completion = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": "你是一个专业的报告生成助手。"},
                {"role": "user", "content": content}
            ],
            model="gpt-4"
        )
        return chat_completion['choices'][0]['message']['content']
