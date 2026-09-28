import os

from openai import OpenAI


class LLM:
    """对话客户端：messages由调用方传入，密钥走环境变量 DEEPSEEK_API_KEY。"""

    def __init__(self, model: str = "deepseek-chat", temperature: float = 0.3):
        self.client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com",
        )
        self.model = model
        self.temperature = temperature

    def chat(self, messages: list) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=False,
        )
        return resp.choices[0].message.content
