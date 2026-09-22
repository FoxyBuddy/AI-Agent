import os

from openai import OpenAI


class LLM:
    def __init__(self):
        pass
    @staticmethod
    def getresp():
        client = OpenAI(
            api_key='sk-245b495fce5844e892edd0372171f9c3',
            base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=[
                {"role": "system", "content": "What's your job?"},
                {"role": "user", "content": "你的职业是什么"},
            ],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}}
        )

        return response.choices[0].message.content