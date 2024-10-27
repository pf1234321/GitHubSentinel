# llm.py
import openai
import os

class LLM:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def summarize_progress(self, content):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一个专业的报告生成助手。"},
                {"role": "user", "content": content}
            ],
            max_tokens=1500,
            temperature=0.5
        )
        return response['choices'][0]['message']['content']
