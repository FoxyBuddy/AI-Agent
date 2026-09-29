import json

from LLM import LLM
from tools import TOOLS_SPEC, execute_tool, truncate

SYSTEM_PROMPT = """你是一个学术论文检索助手。用户给你研究主题或问题，你可以调用工具检索论文。
规则：
1. 先分析用户需求，提炼出合适的英文检索词，再调用工具；
2. 拿到结果后，如果结果太少或明显不相关，可换一个检索词再试；
3. 最后用中文输出综述：每篇论文一行（年份 | 标题 | 一句话概括），结尾给整体小结。"""

MAX_STEPS = 6        # 防失控护栏：最多6轮推理-行动循环
OBS_BUDGET = 4000    # 每次工具结果回填的上下文预算（字符）


def run_agent(user_query: str) -> str:
    """手搓ReAct循环：Reason(模型文本) -> Act(工具调用) -> Observation(结果回填) -> 循环到终答。"""
    llm = LLM()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]
    for step in range(1, MAX_STEPS + 1):
        msg = llm.chat(messages, tools=TOOLS_SPEC)

        if msg.content:                                   # Thought：调用工具前的推理文本
            print(f"[Thought {step}] {msg.content[:120]}")

        if not msg.tool_calls:                            # 出口1：模型给出终答
            return msg.content

        messages.append(msg)                              # 记录模型的行动意图
        for tc in msg.tool_calls:                         # Act：执行每一个工具调用
            name = tc.function.name
            try:
                args = json.loads(tc.function.arguments)
            except json.JSONDecodeError as e:             # 模型输出非法参数：错误回喂，让它自纠
                messages.append({"role": "tool", "tool_call_id": tc.id,
                                 "content": f"参数解析失败: {e}，请输出合法JSON参数"})
                continue
            print(f"[Action {step}] {name}({args})")
            result = execute_tool(name, args)
            observation = truncate(json.dumps(result, ensure_ascii=False), OBS_BUDGET)
            print(f"[Observation {step}] {len(result)}篇 / {len(observation)}字符")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": observation})

    return "达到最大循环步数，强制结束。"                    # 出口2：护栏兜底
