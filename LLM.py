import os

from openai import OpenAI


class LLM:
    """对话客户端：messages由调用方传入，密钥走环境变量 DEEPSEEK_API_KEY。"""

    def __init__(self, model: str = "deepseek-flash", temperature: float = 0.3):
        self.client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com",
        )
        self.model = model
        self.temperature = temperature
        self.last_usage = None   # 最近一次调用的token用量（评测计量用）

    def chat(self, messages: list, tools: list | None = None):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,          # ReAct循环传入工具schema；普通对话为None
            temperature=self.temperature,
            stream=False,
        )
        self.last_usage = getattr(resp, "usage", None)
        return resp.choices[0].message
