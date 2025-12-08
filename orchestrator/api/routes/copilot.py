from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import google.generativeai as genai
import logging
import os
from datetime import datetime

from orchestrator.config import settings
from shared.rag import get_rag_service

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
    rfp_id: Optional[str] = None # Optional RFP ID for document-specific queries
    use_rag: bool = True # Enable RAG by default

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    rag_sources: Optional[List[Dict[str, Any]]] = None # Sources used for RAG


@router.post("/chat", response_model=ChatResponse)
async def chat_with_copilot(request: ChatRequest):
    """
    Chat with the RFP Copilot using Google Gemini with RAG support
    """
    try:
        if not settings.GOOGLE_API_KEY:
             return ChatResponse(
                response="I'm sorry, I am not connected to the AI brain yet (Missing API Key).",
                timestamp=datetime.now()
            )

        # Initialize RAG service
        rag_service = get_rag_service()
        rag_context = ""
        rag_sources = []
        
        # Get last user message for RAG query
        last_user_msg = request.messages[-1].content if request.messages else ""
        
        # Use RAG if enabled and query seems document-related
        if request.use_rag and last_user_msg:
            # Query relevant document chunks
            relevant_chunks = rag_service.query_documents(
                query=last_user_msg,
                rfp_id=request.rfp_id,  # Filter by RFP if provided
                limit=5
            )
            
            if relevant_chunks:
                # Build RAG context from relevant chunks
                rag_context = "\n\n".join([
                    f"[Document Chunk {i+1}]:\n{chunk['text']}"
                    for i, chunk in enumerate(relevant_chunks)
                ])
                
                # Store sources for response
                rag_sources = [
                    {
                        "rfp_id": chunk.get("rfp_id", ""),
                        "score": chunk.get("score", 0),
                        "preview": chunk.get("text", "")[:200] + "..."
                    }
                    for chunk in relevant_chunks
                ]
                
                logger.info(f"Retrieved {len(relevant_chunks)} relevant chunks for RAG")

        # Initialize model
        # Using gemini-2.5-flash as confirmed by list_models
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Construct chat history
        chat_history = []
        
        # System Prompt / Context Injection
        system_instruction = "You are an expert RFP Tender Analyst Copilot. Your goal is to help users understand complex tender documents, technical specifications, and pricing strategies. Be professional, concise, and helpful."
        
        # Add RAG context if available
        if rag_context:
            system_instruction += f"\n\nHere are relevant excerpts from the uploaded RFP documents:\n{rag_context}\n\nUse this information to answer the user's question accurately. If the answer is in the documents, cite the specific information."
        
        # Add manual context if provided
        if request.context:
            system_instruction += f"\n\nAdditional context from the active document:\n{request.context}\n\nAnswer the user's question based on this context if applicable."

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
            "parts": ["Understood. I am ready to act as the RFP Analyst Copilot with access to the uploaded documents."]
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
        response = chat.send_message(last_user_msg)
        
        return ChatResponse(
            response=response.text,
            timestamp=datetime.now(),
            rag_sources=rag_sources if rag_sources else None
        )

    except Exception as e:
        logger.error(f"Error in Copilot chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
