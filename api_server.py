import logging
import os
import traceback
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import logging
import traceback
from typing import Optional, Dict, Any

from faq_bot import FAQBot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Try different possible filenames in order of preference
POSSIBLE_FAQ_FILES = [
    os.path.join(BASE_DIR, "faq_data.xlsx"),  # Preferred name
    os.path.join(BASE_DIR, "faq(1).xlsx"),   # Original name
    os.path.join(BASE_DIR, "faq.xlsx"),      # Simple alternative
]

app = FastAPI()

# Initialize FAQ Bot
faq_bot = None
for faq_file in POSSIBLE_FAQ_FILES:
    try:
        if os.path.exists(faq_file):
            logger.info(f"Attempting to load FAQ data from: {faq_file}")
            faq_bot = FAQBot(faq_file)
            logger.info(f"Successfully loaded {len(faq_bot.questions)} questions from {faq_file}")
            break
        else:
            logger.warning(f"FAQ file not found: {faq_file}")
    except Exception as e:
        logger.error(f"Error loading {faq_file}: {str(e)}")
        logger.error(traceback.format_exc())

if faq_bot is None:
    error_msg = f"Failed to initialize FAQ Bot. Tried the following files: {', '.join(POSSIBLE_FAQ_FILES)}"
    logger.error(error_msg)
    raise RuntimeError(error_msg)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat")
async def chat(chat_request: ChatRequest):
    try:
        message = chat_request.message.strip()
        if not message:
            return JSONResponse(
                status_code=400,
                content={"reply": "Message cannot be empty"}
            )
        
        # Get response from FAQ bot
        reply = faq_bot.answer(message)
        
        return {"reply": reply}
        
    except Exception as e:
        logger.error(f"Error in /chat: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"reply": f"Error: {str(e)}"}
        )


@app.get("/")
async def health():
    try:
        # Test the FAQ bot is working
        test_reply = faq_bot.answer("test")
        response = {
            "status": "ok",
            "service": "ira-faq-bot",
            "questions_loaded": len(faq_bot.questions) if hasattr(faq_bot, 'questions') else 0,
            "test_reply": test_reply[:100] + "..." if len(test_reply) > 100 else test_reply
        }
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "error",
            "service": "ira-faq-bot",
            "error": str(e)
        }, 500
