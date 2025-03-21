from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json

from ..database import get_db
from ..models import Tool, Parameter
from ..schemas import ToolCreate, Tool as ToolSchema, ToolBase
from ..utils.embedding import generate_embedding

router = APIRouter()

@router.get("/tools", response_model=List[ToolSchema])
async def get_tools(db: Session = Depends(get_db)):
    """Get all tools"""
    tools = db.query(Tool).all()
    return tools

@router.get("/tools/{tool_id}", response_model=ToolSchema)
async def get_tool(tool_id: int, db: Session = Depends(get_db)):
    """Get a tool by ID"""
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool

@router.post("/tools", response_model=ToolSchema)
async def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    """Create a new tool"""
    # Check if tool with the same name already exists
    existing_tool = db.query(Tool).filter(Tool.name == tool.name).first()
    if existing_tool:
        raise HTTPException(status_code=400, detail=f"Tool with name '{tool.name}' already exists")
    
    # Generate embedding for the tool description
    embedding = generate_embedding(f"{tool.name}: {tool.description}")
    embedding_json = json.dumps(embedding)
    
    # Create the tool
    db_tool = Tool(
        name=tool.name,
        description=tool.description,
        parameters_schema=tool.parameters_schema,
        is_native=tool.is_native,
        function_path=tool.function_path,
        endpoint_url=tool.endpoint_url,
        embedding=embedding_json
    )
    
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    
    return db_tool

@router.put("/tools/{tool_id}", response_model=ToolSchema)
async def update_tool(tool_id: int, tool: ToolBase, db: Session = Depends(get_db)):
    """Update an existing tool"""
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    # Update the tool
    db_tool.name = tool.name
    db_tool.description = tool.description
    db_tool.parameters_schema = tool.parameters_schema
    
    # Update embedding
    embedding = generate_embedding(f"{tool.name}: {tool.description}")
    db_tool.embedding = json.dumps(embedding)
    
    db.commit()
    db.refresh(db_tool)
    
    return db_tool

@router.delete("/tools/{tool_id}")
async def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    """Delete a tool"""
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    db.delete(db_tool)
    db.commit()
    
    return {"message": f"Tool '{db_tool.name}' deleted successfully"} 