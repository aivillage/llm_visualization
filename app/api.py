from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
from GPTNeoWrap import router as api_router
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def make_app():
    app = FastAPI(
        docs_url=None, # Disable docs (Swagger UI)
        redoc_url=None, # Disable redoc    
    )
    app.mount("/", StaticFiles(directory="app/static"), name="static")
    app.include_router(api_router, prefix="/api")

    