from sqlalchemy import Column, Integer, String, Text, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import json

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    parameters_schema = Column(JSON)  # Stores the JSON schema for parameters
    is_native = Column(Boolean, default=False)  # Indicates if tool is native or custom
    function_path = Column(String, nullable=True)  # Path to function if native
    endpoint_url = Column(String, nullable=True)  # URL for custom tool
    embedding = Column(Text, nullable=True)  # The text embedding as JSON string
    
    # Relationship to parameter model
    parameters = relationship("Parameter", back_populates="tool", cascade="all, delete-orphan")
    
    def to_json_schema(self):
        """Convert the tool to a JSON schema format for LLM interaction"""
        schema = {
            "name": self.name,
            "description": self.description,
            "parameters": json.loads(self.parameters_schema) if isinstance(self.parameters_schema, str) else self.parameters_schema
        }
        return schema


class Parameter(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    parameter_type = Column(String)  # string, number, boolean, etc.
    required = Column(Boolean, default=False)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    
    # Relationship to tool
    tool = relationship("Tool", back_populates="parameters") 