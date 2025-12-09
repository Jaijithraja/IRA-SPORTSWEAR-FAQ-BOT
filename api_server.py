from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from faq_bot import FAQBot

FAQ_PATH = "faq(1).xlsx"

app = FastAPI()
faq_bot = FAQBot(FAQ_PATH)

# Explicit allowed origins
origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "https://ira-sportswear.com",
    "https://www.irasportswear.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,   # keep this False with multiple origins
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = faq_bot.answer(req.message)
    return ChatResponse(reply=reply)


# Optional health check
@app.get("/")
def health():
    return {"status": "ok", "service": "ira-faq-bot"}
