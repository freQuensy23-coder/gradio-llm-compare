from typing import Optional


class DialogHistory:
    default_system_prompt = 'You are AI-assistant'

    def __init__(self, messages: [dict] = None):
        if messages is None:
            messages = []
        self.messages = messages
        pass

    @staticmethod
    def from_gradio(messages: [tuple], new_message: Optional[str] = None, system_prompt: [str] = None):
        obj = DialogHistory()
        if system_prompt:
            obj.messages.append({'role': 'system', 'text': system_prompt})
        else:
            obj.messages.append({'role': 'system', 'text': DialogHistory.default_system_prompt})
        for user_message, bot_message in messages:
            obj.messages.append({'role': 'user', 'text': user_message})
            obj.messages.append({'role': 'bot', 'text': bot_message})
        if new_message:
            obj.messages.append({'role': 'user', 'text': new_message})
        return obj

    @property
    def system_prompt(self):
        return self.messages[0]['text']

    def generate_prompt(self)-> str:
        result = f'{self.system_prompt}\n' + '\n'.join(
            [f'{message["role"]}: {message["text"]}' for message in self.messages[1:]])
        if self.messages[-1]['role'] == 'user':
            result += f'\nbot:'
        return result
