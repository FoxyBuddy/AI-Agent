import gradio as gr
import os
from openai import OpenAI

import LLM


def greet(name, intensity):
    return LLM.LLM.getresp()

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
    api_name="predict"
)

demo.launch()