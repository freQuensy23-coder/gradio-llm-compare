import gradio as gr
import json
import datetime

# Инициализируем список для хранения диалогов
dialogues = []


def add_message(role, message):
    # Добавляем сообщение в список диалогов
    dialogues.append({'role': role, 'content': message})
    # Возвращаем обновленный диалог для отображения в интерфейсе
    if role == "user":
        new_role = "assistant"
    else:
        new_role = "user"
    return "\n".join([f"{d['role']}: {d['content']}" for d in dialogues]), new_role, ''


def save_dialogues():
    global dialogues
    # Сохраняем диалоги в файл
    with open(f'dialogues_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json', 'w', encoding='utf-8') as f:
        json.dump(dialogues, f, ensure_ascii=False, indent=4)
    dialogues = []
    return ""


# Создаем интерфейс
with gr.Blocks() as app:
    with gr.Row():
        user_input = gr.Textbox(label="Ваше сообщение")
        role_select = gr.Radio(choices=["user", "assistant"], value="user", label="Выберите роль")
    add_button = gr.Button("Добавить сообщение")
    dialogue_display = gr.Textbox(label="Диалог", lines=10, interactive=False)
    save_button = gr.Button("Сохранить диалог в файл")

    add_button.click(add_message, inputs=[role_select, user_input], outputs=[dialogue_display, role_select, user_input])
    user_input.submit(add_message, inputs=[role_select, user_input], outputs=[dialogue_display, role_select, user_input])
    save_button.click(save_dialogues, inputs=[], outputs=dialogue_display)

app.launch()
