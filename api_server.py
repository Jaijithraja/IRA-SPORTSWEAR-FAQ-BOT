from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from faq_bot import FAQBot
from fastapi.staticfiles import StaticFiles
import os
# Initialize app
app = FastAPI(title="IRA Sportswear FAQ API")

# Define BASE_DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static",StaticFiles(directory=os.path.join(BASE_DIR,"static")),name="static") 

# Load FAQ bot ONCE at startup
faq_bot = FAQBot("faq(1).xlsx")
# CORS (open for now, restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/health")
def health():
    return {
        "status": "ok",
        "questions_loaded": len(faq_bot.questions)
    }

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = faq_bot.answer(req.message)
    return {"reply": reply}
