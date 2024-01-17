import gradio as gr
from llm import llm1, llm2
from history import DialogHistory


def send_message_callback(user_data: gr.State, chat_area, input_area):
    history = DialogHistory.from_gradio(messages=chat_area, new_message=input_area)
    return llm1(history), llm2(history)


def apply(input_text, applied_output, chat_area):
    return '', '', '', chat_area + [(input_text, applied_output)]