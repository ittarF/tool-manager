import json
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Tool
from .utils.embedding import generate_embedding

def initialize_tools():
    """Initialize the database with sample tools"""
    db = SessionLocal()
    
    try:
        # Check if tools already exist
        existing_tools = db.query(Tool).all()
        if existing_tools:
            print("Tools already initialized")
            return
        
        # Create sample tools
        sample_tools = [
            {
                "name": "get_current_time",
                "description": "Get the current date and time",
                "is_native": True,
                "function_path": "app.tools.native_tools.get_current_time",
                "parameters_schema": {}
            },
            {
                "name": "calculate",
                "description": "Perform a basic calculation operation (add, subtract, multiply, divide)",
                "is_native": True,
                "function_path": "app.tools.native_tools.calculate",
                "parameters_schema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "The operation to perform (add, subtract, multiply, divide)",
                            "enum": ["add", "subtract", "multiply", "divide"]
                        },
                        "x": {
                            "type": "number",
                            "description": "The first number"
                        },
                        "y": {
                            "type": "number",
                            "description": "The second number"
                        }
                    },
                    "required": ["operation", "x", "y"]
                }
            },
            {
                "name": "random_number",
                "description": "Generate a random number within a range",
                "is_native": True,
                "function_path": "app.tools.native_tools.random_number",
                "parameters_schema": {
                    "type": "object",
                    "properties": {
                        "min_value": {
                            "type": "integer",
                            "description": "The minimum value (inclusive)",
                            "default": 1
                        },
                        "max_value": {
                            "type": "integer",
                            "description": "The maximum value (inclusive)",
                            "default": 100
                        }
                    }
                }
            },
            {
                "name": "weather_info",
                "description": "Get mock weather information for a city",
                "is_native": True,
                "function_path": "app.tools.native_tools.weather_info",
                "parameters_schema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The name of the city"
                        }
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "search_text",
                "description": "Search for a query in a text",
                "is_native": True,
                "function_path": "app.tools.native_tools.search_text",
                "parameters_schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to search in"
                        },
                        "query": {
                            "type": "string",
                            "description": "The query to search for"
                        }
                    },
                    "required": ["text", "query"]
                }
            },
            {
                "name": "real_weather",
                "description": "Get real-time weather data for any city using Open-Meteo API",
                "is_native": True,
                "function_path": "app.tools.native_tools.real_weather",
                "parameters_schema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The name of the city"
                        },
                        "country_code": {
                            "type": "string",
                            "description": "Optional two-letter country code (ISO 3166)",
                            "default": None
                        }
                    },
                    "required": ["city"]
                }
            }
        ]
        
        for tool_data in sample_tools:
            # Generate embedding for the tool description
            embedding = generate_embedding(f"{tool_data['name']}: {tool_data['description']}")
            embedding_json = json.dumps(embedding)
            
            # Create the tool
            tool = Tool(
                name=tool_data["name"],
                description=tool_data["description"],
                parameters_schema=tool_data["parameters_schema"],
                is_native=tool_data["is_native"],
                function_path=tool_data["function_path"],
                embedding=embedding_json
            )
            
            db.add(tool)
        
        db.commit()
        print("Sample tools initialized successfully")
    
    finally:
        db.close()

if __name__ == "__main__":
    initialize_tools() 