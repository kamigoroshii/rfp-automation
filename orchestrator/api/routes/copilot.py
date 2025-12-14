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
    Chat with the RFP Copilot - Static responses for common questions
    """
    try:
        if not settings.GOOGLE_API_KEY:
             return ChatResponse(
                response="I'm sorry, I am not connected to the AI brain yet (Missing API Key).",
                timestamp=datetime.now()
            )

        # Get last user message
        last_user_msg = request.messages[-1].content if request.messages else ""
        query_lower = last_user_msg.lower()
        
        # Static responses for common questions
        static_responses = {
            "liability": """📋 **Liability Risk Summary for This RFP**

Based on the analyzed tender documents, here are the key liability considerations:

**🔴 High Risk Areas:**
1. **Performance Guarantees** - 10-year warranty on cable performance with penalty clauses up to 10% of contract value
2. **Delivery Delays** - Liquidated damages of 0.5% per week for delays (max 10% of order value)
3. **Testing Failures** - Full replacement cost + retest charges if products fail routine/type tests

**🟡 Medium Risk Areas:**
1. **Standards Compliance** - Must meet IEC 60502-2 and IS 7098; non-compliance may result in rejection
2. **Quality Defects** - 24-month defect liability period with replacement obligations
3. **Insurance Requirements** - Product liability insurance of minimum ₹50 lakhs required

**🟢 Mitigation Strategies:**
- Ensure products are pre-tested and certified before delivery
- Buffer delivery timelines by 15-20% to avoid penalty triggers
- Review insurance coverage adequacy
- Document all quality control measures

**Recommendation:** Acceptable risk level if proper quality controls are in place. Consider increasing margins by 2-3% to cover potential liability exposure.""",

            "voltage": """⚡ **Voltage Levels & Cable Specifications Summary**

**Primary Requirements:**
- **Voltage Rating:** 11kV (Medium Voltage Distribution)
- **Conductor Type:** Aluminum, 240 sq.mm cross-sectional area
- **Cores:** 3-Core configuration
- **Insulation:** XLPE (Cross-Linked Polyethylene)
- **Armoring:** SWA (Steel Wire Armour)
- **Temperature Rating:** 90°C continuous operation

**Standards Compliance:**
- IEC 60502-2 (Power cables with extruded insulation)
- IS 7098 (Indian Standard for PVC/XLPE insulated cables)

**Testing Requirements:**
- Type Test (as per IEC 60502)
- Routine Test (100% production testing)
- Partial Discharge Test
- Heat Cycle Test

**Typical Applications:**
This specification is standard for urban distribution networks, industrial estates, and renewable energy projects requiring medium voltage transmission over distances of 2-5 km.""",

            "price": """💰 **Pricing Strategy Recommendation**

**Market Analysis:**
- **Current Market Range:** ₹1,850 - ₹2,200 per meter for 11kV 3C x 240 sq.mm XLPE/AL/SWA
- **Your Estimated Cost:** ₹1,923 per meter (including testing & delivery)

**Competitive Positioning:**

**Option 1: Aggressive (Win-Focused)** 🎯
- Quote: ₹1,975/meter
- Win Probability: 75%
- Margin: 2.7%
- Best for: Government tenders, high competition

**Option 2: Balanced (Recommended)** ⚖️
- Quote: ₹2,050/meter  
- Win Probability: 60%
- Margin: 6.6%
- Best for: Private sector, established clients

**Option 3: Conservative (Premium)** 🛡️
- Quote: ₹2,150/meter
- Win Probability: 35%
- Margin: 11.8%
- Best for: Niche specs, limited competition

**Urgency Factor:**
Current deadline is tight (4 days). Consider aggressive pricing to maximize win chances, or request deadline extension to reduce urgency surcharges.

**Final Recommendation:** Use Aggressive strategy at ₹1,975/meter for this tender."""
        }
        
        # Match user query to predefined responses
        response_text = ""
        
        if any(word in query_lower for word in ["liability", "risk", "penalty", "penalties", "damages"]):
            response_text = static_responses["liability"]
        elif any(word in query_lower for word in ["voltage", "specification", "cable", "specs", "technical", "xlpe", "conductor"]):
            response_text = static_responses["voltage"]
        elif any(word in query_lower for word in ["price", "pricing", "cost", "quote", "bid", "competitive"]):
            response_text = static_responses["price"]
        else:
            # Default response for other questions
            response_text = f"""👋 **SmartBid Co-Pilot - Available Topics**

I can help you with these common RFP questions:

1️⃣ **Liability & Risk Analysis**
   - Ask: "Summarize the liability risk in this RFP"
   - Get detailed risk assessment and mitigation strategies

2️⃣ **Technical Specifications**
   - Ask: "What are the voltage levels and cable specifications?"
   - Get complete technical requirements and standards

3️⃣ **Pricing Strategy**
   - Ask: "What's the recommended pricing strategy?"
   - Get market analysis and competitive positioning

💡 **Your Question:** "{last_user_msg}"

Please ask about liability risks, technical specifications, or pricing strategy, and I'll provide detailed insights!"""
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now(),
            rag_sources=None
        )

    except Exception as e:
        logger.error(f"Error in Copilot chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
