from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import torch, simplejson
    
def pretty_floats(obj):
    if isinstance(obj, float):
        return f'{obj:.4f}'
    elif isinstance(obj, dict):
        return dict((k, pretty_floats(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return list(map(pretty_floats, obj))
    return obj

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
    

    def forward(self, text: str) -> str:
        token_ids = self.tokenizer.encode(text)
        tokens = self.tokenizer(text, return_tensors="pt")
        tokens.to(self.model.device)
        output = self.model.transformer(**tokens, output_hidden_states=True)
        embedding = output.hidden_states[0].detach()[0]
        context = output.last_hidden_state.detach()[0]
        embedding = torch.fft.fft(embedding, dim=1).real.numpy()
        context = torch.fft.fft(context, dim=1).real.numpy()
        embedding = embedding[:, :20]
        context = context[:, :20]


        logits = self.model.lm_head(output.last_hidden_state)
        logits = torch.softmax(logits[0,-1,:], dim=-1)
        logits = torch.topk(logits, k=5, dim=-1)
        top_k_generated_token_id = logits.indices
        top_k_generated_token = self.displayable_tokens(top_k_generated_token_id)
        top_k_generated_token_logits = logits.values

        return simplejson.dumps({
            "tokens": self.displayable_tokens(token_ids),
            "token_ids": token_ids,
            "embedding": pretty_floats(embedding.round(decimals=4).tolist()),
            "context": pretty_floats(context.round(decimals=4).tolist()),
            "logits": {
                "top_k": top_k_generated_token,
                "top_k_ids": top_k_generated_token_id.tolist(),
                "top_k_logits": pretty_floats(top_k_generated_token_logits.round(decimals=4).tolist()),
            }
        })