from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..database import get_db
from ..models import Tool
from ..schemas import ToolLookupRequest, ToolLookupResponse, ToolSchema
from ..utils.embedding import generate_embedding, compute_similarity
import json

router = APIRouter()

@router.post("/tool_lookup", response_model=ToolLookupResponse)
async def lookup_tools(request: ToolLookupRequest, db: Session = Depends(get_db)):
    """Find tools relevant to a user prompt using embedding similarity"""
    
    # Generate embedding for the prompt
    prompt_embedding = generate_embedding(request.prompt)
    
    # Get all tools from the database
    tools = db.query(Tool).all()
    
    if not tools:
        return ToolLookupResponse(tools=[])
    
    # Prepare tool data for similarity comparison
    tool_data = []
    for tool in tools:
        # Parse the embedding if it exists
        embedding = None
        if tool.embedding:
            try:
                embedding = json.loads(tool.embedding)
            except json.JSONDecodeError:
                continue
        
        tool_data.append({
            "id": tool.id,
            "name": tool.name,
            "description": tool.description,
            "parameters_schema": tool.parameters_schema,
            "embedding": embedding
        })
    
    # Compute similarity and get top_k tools
    similar_tools = compute_similarity(prompt_embedding, tool_data, request.top_k)
    
    # Convert to response format
    tool_schemas = []
    for tool_info in similar_tools:
        # Get the full tool from the database
        tool = db.query(Tool).filter(Tool.id == tool_info["id"]).first()
        if tool:
            tool_schemas.append(
                ToolSchema(
                    name=tool.name,
                    description=tool.description,
                    parameters=json.loads(tool.parameters_schema) if isinstance(tool.parameters_schema, str) else tool.parameters_schema
                )
            )
    
    return ToolLookupResponse(tools=tool_schemas) 