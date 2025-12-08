from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import google.generativeai as genai
import logging
import os
from datetime import datetime

from orchestrator.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Configure Google Gemini
if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
else:
    logger.warning("GOOGLE_API_KEY not found. Copilot will not function correctly.")

router = APIRouter()

class Message(BaseModel):
    role: str # 'user' or 'model'
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    messages: List[Message]
    context: Optional[str] = None # Optional RAG context if we want to pass specific text

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime


@router.post("/chat", response_model=ChatResponse)
async def chat_with_copilot(request: ChatRequest):
    """
    Chat with the RFP Copilot using Google Gemini
    """
    try:
        if not settings.GOOGLE_API_KEY:
             return ChatResponse(
                response="I'm sorry, I am not connected to the AI brain yet (Missing API Key).",
                timestamp=datetime.now()
            )

        # Initialize model
        # Using gemini-2.5-flash as confirmed by list_models
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Construct chat history
        chat_history = []
        
        # System Prompt / Context Injection
        system_instruction = "You are an expert RFP Tender Analyst Copilot. Your goal is to help users understand complex tender documents, technical specifications, and pricing strategies. Be professional, concise, and helpful."
        
        if request.context:
            system_instruction += f"\n\nHere is the relevant context from the active document:\n{request.context}\n\nAnswer the user's question based on this context if applicable."

        # Since Gemini (python-sdk) uses a specific history format, we adapt:
        # History format: [{'role': 'user', 'parts': [...]}, {'role': 'model', 'parts': [...]}]
        # We'll treat the system instruction as the first user message for simplicity (or use system_instruction if supported in beta)
        
        # Simplest approach: Concatenate all history into a strict prompt if 'chat' mode is complex, 
        # but using start_chat is better for maintaining session.
        
        history_for_gemini = []
        
        # Add system context as first message context
        history_for_gemini.append({
            "role": "user",
            "parts": [system_instruction]
        })
        history_for_gemini.append({
            "role": "model",
            "parts": ["Understood. I am ready to act as the RFP Analyst Copilot."]
        })

        # Add recent conversation history (Limit to last 10 messages to avoid token limits)
        for msg in request.messages[:-1]: # Exclude the very last one as that is the prompt
            role = "user" if msg.role == "user" else "model"
            history_for_gemini.append({
                "role": role,
                "parts": [msg.content]
            })

        chat = model.start_chat(history=history_for_gemini)
        
        # Send new message
        last_user_msg = request.messages[-1].content
        response = chat.send_message(last_user_msg)
        
        return ChatResponse(
            response=response.text,
            timestamp=datetime.now()
        )

    except Exception as e:
        logger.error(f"Error in Copilot chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
