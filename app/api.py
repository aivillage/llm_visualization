from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
from GPTNeoWrap import GPTNeoWrap
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

current = "EleutherAI/gpt-neo-1.3B"

model = AutoModelForCausalLM.from_pretrained(current)
tokenizer = AutoTokenizer.from_pretrained(current)

wrap = GPTNeoWrap(model=model, tokenizer=tokenizer)

class RequestBody(BaseModel):
    userInput: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/", response_class=ORJSONResponse)
async def root(req: RequestBody):
    print(req.userInput)
    return wrap.forward(req.userInput)

@app.get("/test")
async def root():
    return {"message": "Hello World"}
