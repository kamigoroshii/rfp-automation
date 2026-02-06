# 🔍 RAG (Retrieval-Augmented Generation) Implementation Guide

## 📚 Overview

This project implements a **hybrid RAG system** for product matching and document querying. It combines:
1. **Vector-based semantic search** (Qdrant + Sentence Transformers)
2. **Rule-based matching** (fallback mechanism)
3. **Document chunking and retrieval** (for RFP PDFs)

---

## 🏗️ Architecture

### Two RAG Systems in This Project

#### 1. **Product Catalog RAG** (`agents/technical/agent.py`)
- **Purpose**: Match RFP specifications to product SKUs
- **Vector DB**: Qdrant
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **Collection**: `products`

#### 2. **Document RAG** (`shared/rag/document_rag.py`)
- **Purpose**: Query RFP PDF content semantically
- **Vector DB**: Qdrant
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **Collection**: `rfp_documents`

---

## 🔧 How It Works

### Product Catalog RAG Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. INDEXING PHASE (One-time setup)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  Product Catalog (JSON/Database)      │
    │  - SKU: XLPE-11KV-185                 │
    │  - Name: 11kV XLPE Cable              │
    │  - Specs: {voltage: 11kV, ...}        │
    └───────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  Create Text Representation           │
    │  "11kV XLPE Cable Copper 3 core..."   │
    └───────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  Generate Embedding (384-dim vector)  │
    │  [0.23, -0.45, 0.67, ...]             │
    └───────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  Store in Qdrant                      │
    │  ID: 0                                │
    │  Vector: [0.23, -0.45, ...]           │
    │  Payload: {sku, name, specs}          │
    └───────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  2. QUERY PHASE (Runtime)                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  RFP Specifications                   │
    │  "11kV XLPE Copper conductor cable"   │
    └───────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  Generate Query Embedding             │
    │  [0.25, -0.43, 0.65, ...]             │
    └───────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  Qdrant Cosine Similarity Search      │
    │  Find top-K nearest vectors           │
    └───────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────┐
    │  Return Matched Products              │
    │  1. XLPE-11KV-185 (score: 0.94)       │
    │  2. XLPE-11KV-240 (score: 0.87)       │
    │  3. XLPE-11KV-300 (score: 0.82)       │
    └───────────────────────────────────────┘
```

---

## 📁 Key Files

### 1. Technical Agent (`agents/technical/agent.py`)

**Key Methods:**

```python
class TechnicalAgent:
    def initialize_embedding_model(self):
        """Load sentence-transformers model"""
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def initialize_vector_db(self):
        """Connect to Qdrant"""
        self.vector_db = QdrantClient(host="localhost", port=6333)
    
    def semantic_search(self, query: str, top_k: int = 10):
        """
        1. Generate embedding for query
        2. Search Qdrant for similar vectors
        3. Return top-K products
        """
        vector = self.embedding_model.encode(query).tolist()
        results = self.vector_db.search(
            collection_name="products",
            query_vector=vector,
            limit=top_k
        )
        return results
```

**Hybrid Approach:**
```python
def match_products(self, specifications):
    # Try vector search first
    if self.vector_db and self.embedding_model:
        matches = self.semantic_search(query, top_k)
    
    # Fallback to rule-based if vector search fails
    if not matches:
        matches = self._rule_based_matching(specifications, top_k)
    
    return matches
```

---

### 2. Product Loader (`agents/technical/product_loader.py`)

**Purpose**: Load products into Qdrant

```python
def load_products_qdrant(products):
    # 1. Initialize
    client = QdrantClient(host="localhost", port=6333)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. Create collection
    client.create_collection(
        collection_name="products",
        vectors_config=VectorParams(
            size=384,  # Embedding dimension
            distance=Distance.COSINE  # Similarity metric
        )
    )
    
    # 3. Generate embeddings and upload
    for product in products:
        # Create text representation
        text = f"{product['name']} {product['specs']} {product['description']}"
        
        # Generate embedding
        vector = model.encode(text).tolist()
        
        # Upload to Qdrant
        client.upsert(
            collection_name="products",
            points=[PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "sku": product['sku'],
                    "name": product['name'],
                    "specs": product['specs']
                }
            )]
        )
```

---

### 3. Document RAG Service (`shared/rag/document_rag.py`)

**Purpose**: Ingest and query RFP PDFs

```python
class DocumentRAGService:
    def ingest_document(self, pdf_path, rfp_id):
        """
        1. Extract text from PDF
        2. Split into chunks (500 chars with 100 overlap)
        3. Generate embeddings for each chunk
        4. Store in Qdrant
        """
        text = self.extract_text_from_pdf(pdf_path)
        chunks = self.chunk_text(text)
        
        for chunk in chunks:
            embedding = self.embedding_model.encode(chunk).tolist()
            self.client.upsert(
                collection_name="rfp_documents",
                points=[PointStruct(
                    id=uuid.uuid4(),
                    vector=embedding,
                    payload={
                        "rfp_id": rfp_id,
                        "text": chunk,
                        "pdf_path": pdf_path
                    }
                )]
            )
    
    def query_documents(self, query, rfp_id=None, limit=5):
        """
        1. Generate query embedding
        2. Search Qdrant for similar chunks
        3. Return top-K relevant chunks
        """
        query_embedding = self.embedding_model.encode(query).tolist()
        
        results = self.client.search(
            collection_name="rfp_documents",
            query_vector=query_embedding,
            query_filter=Filter(must=[
                FieldCondition(key="rfp_id", match=MatchValue(value=rfp_id))
            ]),
            limit=limit
        )
        
        return results
```

---

## 🚀 How to Use This RAG in Another Project

### Step 1: Install Dependencies

```bash
pip install qdrant-client sentence-transformers PyPDF2
```

### Step 2: Start Qdrant

**Option A: Docker**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Option B: Local Installation**
```bash
# Download from https://qdrant.tech/documentation/quick-start/
./qdrant
```

### Step 3: Copy RAG Components

**Minimal Setup (Copy these files):**
```
your_project/
├── rag/
│   ├── __init__.py
│   ├── document_rag.py          # Copy from shared/rag/
│   └── product_rag.py           # Adapt from agents/technical/agent.py
└── requirements.txt
```

### Step 4: Initialize RAG Service

```python
from rag.document_rag import DocumentRAGService

# Initialize
rag = DocumentRAGService()

# Ingest a document
rag.ingest_document(
    pdf_path="path/to/document.pdf",
    rfp_id="DOC-001",
    metadata={"title": "My Document", "source": "email"}
)

# Query the document
results = rag.query_documents(
    query="What are the technical specifications?",
    rfp_id="DOC-001",
    limit=5
)

for result in results:
    print(f"Score: {result['score']}")
    print(f"Text: {result['text']}")
    print("---")
```

---

## 🎯 Standalone RAG Template

Here's a **minimal, standalone RAG implementation** you can use:

```python
"""
Minimal RAG Implementation
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import uuid

class SimpleRAG:
    def __init__(self, collection_name="documents"):
        # Initialize
        self.client = QdrantClient(host="localhost", port=6333)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection_name = collection_name
        
        # Create collection
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE
                )
            )
        except:
            pass  # Collection already exists
    
    def add_text(self, text: str, metadata: dict = None):
        """Add text to RAG"""
        # Generate embedding
        vector = self.model.encode(text).tolist()
        
        # Store in Qdrant
        selults[0]["tnt(res
priython?")at is Pry("Wh rag.ques =ry
result"})

# Quey": "AIorategthms", {"c algorisese learning uMachintext("
rag.add_: "tech"})ategory"uage", {"cang lnggrammin is a proho("Pytxt
rag.add_tedd documentsAG()

# AleRSimp
rag = age  ]

# Us  lts
     r in resuor  f     }
                 ext"}
 if k != "t.items() r.payloador k, v in {k: v fata":  "metad        
      ,e": r.score      "scor        ],
  xt"load["teext": r.pay         "t    {
             urn [
       ret   sults
turn re    # Re   
        )
     t
    t=limi  limi       ctor,
   uery_veector=qry_v     que      e,
 n_namctiole.collfe=selection_nam    col       h(
 nt.searc = self.clieresults       Search
   #       
        
()istn).tole(questioencododel.tor = self.m_vec    queryg
    y embeddiner querateGen#     """
    ""Query RAG      " = 5):
  t: intmi str, liquestion:(self,  query
    def)
                   )]
    a or {})}
 *(metadattext, *{"text":    payload=         r,
    ctor=vecto         ve     ()),
  uid.uuid4r(ud=st      i     uct(
     intStrodels.Pooints=[m          p,
  n_nameioollectname=self.clection_        colert(
    f.client.ups