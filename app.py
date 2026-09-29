import gradio as gr

from agent import run_agent

demo = gr.Interface(
    fn=run_agent,
    inputs=gr.Textbox(label="研究主题", placeholder="例如：3D点云对抗攻击与防御"),
    outputs=gr.Markdown(label="文献综述"),
    title="AI Agent 论文检索助手",
    description="ReAct循环（思考→行动→观察）+ Crossref学术检索，自动检索并综述论文。",
)

if __name__ == "__main__":
    demo.launch()
