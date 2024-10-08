import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from backtrack_sampler import BacktrackSampler
from strategy.antislop_strategy import AntiSlopStrategy

model_name = "unsloth/Llama-3.2-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = torch.device('cuda')

slops = [
    'kaleidoscope',
    'symphony',
    'testament to',
    'elara',
    'moth to a flame'
]
prompt_text = "Write a story about Elara, the weaver of tapestries in future Technopolis. In the bustling city, a group of "
messages = [
    {"role": "user", "content": prompt_text}
]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
strategy = AntiSlopStrategy(tokenizer, slops)
sampler = BacktrackSampler(model, tokenizer, strategy, device)

token_stream = sampler.generate(
    prompt=prompt,
    max_new_tokens=128,
    temperature=1
)

for tokens in token_stream:
    print(tokenizer.decode(tokens, skip_special_tokens=True), end="", flush=True)