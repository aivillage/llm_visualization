from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

address = '0.0.0.0'
port = 50055
current = "EleutherAI/gpt-neo-125M"

model = AutoModelForCausalLM.from_pretrained(current)
tokenizer = AutoTokenizer.from_pretrained(current)

class GPTNeoWrap:
    model: AutoModelForCausalLM
    tokenizer: AutoTokenizer

    def __init__(self, *, model: AutoModelForCausalLM, tokenizer: AutoTokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def forward(self, text: str) -> torch.tensor:
        tokens = self.tokenizer(text, return_tensors="pt")
        tokens.to(self.model.device)
        return self.model.transformer(**tokens, output_hidden_states=True)
    
wrap = GPTNeoWrap(model=model, tokenizer=tokenizer)

print(wrap.forward("the quick brown fox"))