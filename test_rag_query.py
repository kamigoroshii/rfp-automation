"""Test RAG query capability"""
from shared.rag import get_rag_service

rag = get_rag_service()
print('RAG Service Status:')
print(f'Collection: {rag.collection_name}')

# Test query
chunks = rag.query_documents('11kV cable specifications', limit=3)
print(f'\nFound {len(chunks)} chunks')

for i, chunk in enumerate(chunks):
    print(f'\nChunk {i+1}:')
    print(f'  RFP ID: {chunk.get("rfp_id", "N/A")}')
    print(f'  Score: {chunk.get("score", 0):.3f}')
    print(f'  Text preview: {chunk.get("text", "")[:150]}...')
