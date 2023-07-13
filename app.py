from typing import List
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

    def displayable_tokens(self, tokens: List[int]) -> List[str]:
        def raw(string: str, replace: bool = False) -> str:
            """Returns the raw representation of a string. If replace is true, replace a single backslash's repr \\ with \."""
            r = repr(string)[1:-1]  # Strip the quotes from representation
            if replace:
                r = r.replace('\\\\', '\\')
            return r
        return [raw(self.tokenizer.convert_tokens_to_string([token])) for token in self.tokenizer.convert_ids_to_tokens(tokens)]
    

    def forward(self, text: str) -> torch.tensor:
        token_ids = self.tokenizer.encode(text)
        token_strs = self.displayable_tokens(token_ids)
        tokens = self.tokenizer(text, return_tensors="pt")
        tokens.to(self.model.device)
        output = self.model.transformer(**tokens, output_hidden_states=True)
        embedding = output.hidden_states[0].shape
        context = output.hidden_states[-1].shape

        logits = self.model.lm_head(output.hidden_states[-1])[-1,-1,:]
        logits = torch.topk(logits, k=5, dim=-1)
        top_k_generated_token_id = logits.indices
        print(top_k_generated_token_id)
        top_k_generated_token = self.displayable_tokens(top_k_generated_token_id)
        top_k_generated_token_logits = logits.values

        return {
            "tokens": token_strs,
            "token_ids": token_ids,
            "embedding": embedding,
            "context": context,
            "logits": {
                "top_k": top_k_generated_token,
                "top_k_ids": top_k_generated_token_id,
                "top_k_logits": top_k_generated_token_logits,
            }
        }

    
wrap = GPTNeoWrap(model=model, tokenizer=tokenizer)
output = wrap.forward("the quick brown fox")

print(output)