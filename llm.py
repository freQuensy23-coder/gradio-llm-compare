import torch

from history import DialogHistory
import transformers

model1 = transformers.AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-7b-hf',
                                                           torch_dtype=torch.float16)
tokenizer1 = transformers.AutoTokenizer.from_pretrained('meta-llama/Llama-2-7b-hf')
model1 = model1.to('cuda')

model2 = transformers.AutoModelForCausalLM.from_pretrained('mistralai/mistral-7b-instruct-v0.1',
                                                           torch_dtype=torch.float16)
tokenizer2 = transformers.AutoTokenizer.from_pretrained('mistralai/mistral-7b-instruct-v0.1')
model2 = model2.to('cuda')


def llm1(history: DialogHistory) -> str:
    prompt = history.generate_prompt()
    input_ids = tokenizer1(prompt, return_tensors='pt')
    gen_ids = model1.generate(**input_ids.to(model1.device), temperature=1)[len(input_ids):]
    gen_text = tokenizer1.decode(gen_ids[0])
    return gen_text


def llm2(history: DialogHistory) -> str:
    prompt = history.generate_prompt()
    input_ids = tokenizer2(prompt, return_tensors='pt')
    gen_ids = model2.generate(**input_ids.to(model2.device), temperature=1)[len(input_ids):]
    gen_text = tokenizer2.decode(gen_ids[0])
    return gen_text