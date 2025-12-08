# RFP Automation System - RAG Setup Guide

## Problem
The chatbot cannot access PDFs because:
1. RAG dependencies are missing
2. PDFs are not being automatically ingested
3. Qdrant vector database is not set up

## Solution

### Option 1: Quick Fix (Simplified RAG without Qdrant)

If you want the chatbot to work immediately without setting up Qdrant, we can implement a simpler in-memory RAG:

**Install dependencies:**
```bash
pip install PyPDF2 sentence-transformers
```

This will allow basic PDF text extraction and similarity search in memory.

### Option 2: Full RAG Setup (Recommended for Production)

**Step 1: Install Dependencies**
```bash
pip install qdrant-client sentence-transformers PyPDF2
```

**Step 2: Install & Start Qdrant**

**Windows (Docker):**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**OR Standalone:**
Download from: https://qdrant.tech/documentation/quick-start/

**Step 3: Verify Qdrant is Running**
Visit: http://localhost:6333/dashboard

## What Each Component Does:

- **PyPDF2**: Extracts text from PDF files
- **sentence-transformers**: Converts text to embeddings for semantic search  
- **qdrant-client**: Stores and searches document embeddings
- **Qdrant Server**: Vector database for storing PDF content

## Auto-Ingestion

The system should automatically:
1. Extract text from PDFs when RFPs are uploaded
2. Split text into chunks
3. Generate embeddings
4. Store in Qdrant for RAG queries

## Current Status

✅ RAG service code exists (shared/rag/document_rag.py)
✅ Copilot endpoint configured (orchestrator/api/routes/copilot.py)
❌ Dependencies not installed
❌ PDFs not being auto-ingested
❌ Qdrant server not running

## Recommendation

For immediate testing, I can implement **Option 1** (simplified RAG) which doesn't require Qdrant and works entirely in memory.

Would you like me to implement the simplified version now?
