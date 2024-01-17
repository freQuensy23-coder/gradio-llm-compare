from typing import Optional

import transformers
from jinja2 import TemplateError


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
            obj.messages.append({'role': 'system', 'content': system_prompt})
        else:
            obj.messages.append({'role': 'system', 'content': DialogHistory.default_system_prompt})
        for user_message, assistant_message in messages:
            obj.messages.append({'role': 'user', 'content': user_message})
            obj.messages.append({'role': 'assistant', 'content': assistant_message})
        if new_message:
            obj.messages.append({'role': 'user', 'content': new_message})
        return obj

    @property
    def system_prompt(self):
        return self.messages[0]['content']

    def generate_prompt(self) -> str:
        result = f'{self.system_prompt}\n' + '\n'.join(
            [f'{message["role"]}: {message["content"]}' for message in self.messages[1:]])
        if self.messages[-1]['role'] == 'user':
            result += f'\nassistant:'
        return result

    def apply_chat_template(self, tokenizer: transformers.PreTrainedTokenizer):
        messages = self.messages.copy()
        try:
            return tokenizer.decode(tokenizer.apply_chat_template(messages), skip_special_tokens=True)
        except TemplateError:
            # Some tokenizers do not support a system message
            return messages[0]['content'] + '\n' + tokenizer.decode(tokenizer.apply_chat_template(messages[1:]), skip_special_tokens=True)