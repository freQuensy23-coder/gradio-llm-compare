import gradio as gr
import callbacks


with gr.Blocks() as app:
    user_data = gr.State()
    chat_area = gr.Chatbot()
    with gr.Row():
        with gr.Column(scale=1):
            text1 = gr.Textbox(interactive=False, label='First answer', lines=3)
            btn1 = gr.Button('Apply first')
        with gr.Column(scale=1):
            text2 = gr.Textbox(interactive=False, label='Second answer', lines=3)
            btn2 = gr.Button('Apply second')
    input_area = gr.Textbox(lines=1, label='Text input', placeholder='Type here and press Enter...', interactive=None)

    input_area.submit(fn=callbacks.send_message_callback,
                      inputs=[user_data, chat_area, input_area],
                      outputs=[text1, text2])

    btn1.click(fn=callbacks.apply,
               inputs=[input_area, text1, chat_area],
               outputs=[input_area, text1, text2, chat_area])
    btn2.click(fn=callbacks.apply,
               inputs=[input_area, text2, chat_area],
               outputs=[input_area, text1, text2, chat_area])

app.launch(share=True)
