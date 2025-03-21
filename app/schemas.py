from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union


class ParameterBase(BaseModel):
    name: str
    description: str
    parameter_type: str
    required: bool = False


class ParameterCreate(ParameterBase):
    pass


class Parameter(ParameterBase):
    id: int
    tool_id: int

    class Config:
        from_attributes = True


class ToolBase(BaseModel):
    name: str
    description: str
    parameters_schema: Dict[str, Any] = Field(default_factory=dict)


class ToolCreate(ToolBase):
    is_native: bool = False
    function_path: Optional[str] = None
    endpoint_url: Optional[str] = None


class Tool(ToolBase):
    id: int
    is_native: bool
    function_path: Optional[str] = None
    endpoint_url: Optional[str] = None
    parameters: List[Parameter] = []

    class Config:
        from_attributes = True


class ToolSchema(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]


# Schemas for tool lookup
class ToolLookupRequest(BaseModel):
    prompt: str
    top_k: int = 3


class ToolLookupResponse(BaseModel):
    tools: List[ToolSchema]


# Schemas for tool usage
class ToolCallParameter(BaseModel):
    name: str
    value: Any


class ToolCall(BaseModel):
    name: str
    parameters: Dict[str, Any]


class ToolUsageRequest(BaseModel):
    tool_call: ToolCall


class ToolUsageResponse(BaseModel):
    result: Any
    error: Optional[str] = None 