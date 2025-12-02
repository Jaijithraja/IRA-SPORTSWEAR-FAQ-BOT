# IRA Sportswear FAQ Chatbot

This project is an FAQ-based chatbot using embeddings, built for integration with IRA's Shopify store.

## Features
- Load FAQ from Excel
- Embedding-based question matching
- FastAPI backend with /chat endpoint
- Frontend integration via JS widget
- Test UI (test_chat.html)

## Run locally
uvicorn api_server:app --reload --port 8000
