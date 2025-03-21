from sentence_transformers import SentenceTransformer
import numpy as np
import json
from typing import List, Dict, Any

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> List[float]:
    """Generate an embedding for a text using sentence transformer"""
    embedding = model.encode(text)
    return embedding.tolist()

def compute_similarity(query_embedding: List[float], tool_embeddings: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Compute similarity between query embedding and tool embeddings
    Returns top_k most similar tools
    """
    if not tool_embeddings:
        return []
    
    query_embedding = np.array(query_embedding)
    
    similarities = []
    for tool in tool_embeddings:
        # Skip tools without embeddings
        if not tool.get('embedding'):
            continue
            
        # Convert string embedding to list if needed
        embedding = tool['embedding']
        if isinstance(embedding, str):
            embedding = json.loads(embedding)
        
        # Compute cosine similarity
        tool_embedding = np.array(embedding)
        similarity = np.dot(query_embedding, tool_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(tool_embedding)
        )
        
        similarities.append((similarity, tool))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    # Return top_k tools
    return [item[1] for item in similarities[:top_k]] 