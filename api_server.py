from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from faq_bot import FAQBot

FAQ_PATH = "faq(1).xlsx"

app = FastAPI()
faq_bot = FAQBot(FAQ_PATH)

# allow frontend from Shopify domain to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, put your shop domain here
    allow_credentials=True,
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
