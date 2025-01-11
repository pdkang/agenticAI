# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from .financial_agent import create_agents

app = FastAPI(title="Financial Agent API")

class StockRequest(BaseModel):
    ticker: str

@app.get("/")
async def root():
    return {"message": "Financial Agent API is running"}

@app.post("/analyze")
async def analyze_stock(request: StockRequest):
    try:
        # Create agents
        multi_ai_agent = create_agents()
        
        # Generate query
        query = f"Summarize analyst recommendation and share the latest news for {request.ticker}"
        
        # Get response (note: we need to capture the streamed response)
        response = ""
        for chunk in multi_ai_agent.run(query):
            if isinstance(chunk, str):
                response += chunk
        
        return {"ticker": request.ticker, "analysis": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))