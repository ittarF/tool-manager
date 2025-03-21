from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..database import get_db
from ..models import Tool
from ..schemas import ToolUsageRequest, ToolUsageResponse
from ..utils.tool_executor import execute_tool

router = APIRouter()

@router.post("/tool_usage", response_model=ToolUsageResponse)
async def use_tool(request: ToolUsageRequest, db: Session = Depends(get_db)):
    """Execute a tool call and return the result"""
    
    # Get the tool from the database
    tool = db.query(Tool).filter(Tool.name == request.tool_call.name).first()
    
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool '{request.tool_call.name}' not found")
    
    # Execute the tool
    result, error = execute_tool(
        tool_name=tool.name,
        parameters=request.tool_call.parameters,
        is_native=tool.is_native,
        function_path=tool.function_path,
        endpoint_url=tool.endpoint_url
    )
    
    if error:
        return ToolUsageResponse(result=None, error=error)
    
    return ToolUsageResponse(result=result) 