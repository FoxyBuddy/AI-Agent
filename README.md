# AI-Agent 论文检索助手

基于大模型API的手搓ReAct Agent：输入研究主题，自动检索学术论文并生成中文综述。

## 架构

```
app.py (Gradio界面)
  └─ agent.py  —— ReAct循环：Thought → Action → Observation，最多6轮
       ├─ LLM.py   —— DeepSeek客户端（原生Function Calling，密钥走环境变量）
       └─ tools.py —— 学术检索工具（Crossref后端）：限流休眠 / 按DOI去重 / 摘要截断
```

## 已实现

- **ReAct推理循环**：原生Function Calling承载协议，思考-行动-观察可观测（控制台trace）
- **工具调用**：学术论文检索（标题/摘要/DOI/年份/期刊信息）
- **限流休眠**：请求间隔控制，避免触发服务端限流
- **按DOI去重**：跨调用记忆，同一篇论文不重复出现
- **上下文预算管理**：摘要截断（500字符）+ 工具结果回填截断（4000字符）
- **异常自纠**：模型输出非法工具参数时，错误回喂触发下一轮自我修正
- **防失控护栏**：MAX_STEPS最大循环轮数

## 运行

```bash
pip install openai requests gradio
# Windows: setx DEEPSEEK_API_KEY "你的key"（重开终端）；Linux/Mac: export DEEPSEEK_API_KEY=...
python app.py
```

## 设计决策与踩坑记录

见 [DESIGN.md](DESIGN.md)：arXiv WAF换源决策、API密钥安全、JATS标签清理、自纠机制等。

## Roadmap

- [ ] RAG：检索结果向量化入库（Qdrant）+ 混合检索（向量+关键词）+ 重排序
- [ ] 用户偏好记忆
- [ ] 多Agent协同（检索员 + 综述员）
- [ ] LangChain重写版（与手搓版对比）

## 已知限制

- 检索相关性依赖单轮关键词质量，复杂主题可能需要多轮换词（当前由模型自主决定）
- 无本地缓存：相同主题重复提问会因去重机制返回空（详见DESIGN.md D1，RAG落地后演化为本地优先检索）
