"""
Example script demonstrating how to register a new tool directly using Python
"""
import json
from app.database import SessionLocal
from app.models import Tool
from app.utils.embedding import generate_embedding

def register_new_tool_directly():
    """Register a new tool directly using Python code"""
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Example 1: Adding a new native tool with implementation
        tool_name = "generate_password"
        tool_description = "Generate a random password with specified length and complexity"
        
        # First, check if the tool already exists
        existing_tool = db.query(Tool).filter(Tool.name == tool_name).first()
        if existing_tool:
            print(f"Tool '{tool_name}' already exists in the database")
            return
        
        # Create parameters schema
        parameters_schema = {
            "type": "object",
            "properties": {
                "length": {
                    "type": "integer",
                    "description": "Length of the password",
                    "default": 12
                },
                "include_numbers": {
                    "type": "boolean",
                    "description": "Whether to include numbers in the password",
                    "default": True
                },
                "include_special_chars": {
                    "type": "boolean",
                    "description": "Whether to include special characters in the password",
                    "default": True
                }
            }
        }
        
        # Generate embedding for tool discovery
        embedding = generate_embedding(f"{tool_name}: {tool_description}")
        embedding_json = json.dumps(embedding)
        
        # Create the tool
        new_tool = Tool(
            name=tool_name,
            description=tool_description,
            parameters_schema=parameters_schema,
            is_native=True,
            function_path="app.tools.security_utils.generate_password",
            embedding=embedding_json
        )
        
        # Add and commit to the database
        db.add(new_tool)
        db.commit()
        db.refresh(new_tool)
        
        print(f"Tool '{tool_name}' registered successfully!")
        print(f"ID: {new_tool.id}")
        print(f"Description: {new_tool.description}")
        print(f"Function Path: {new_tool.function_path}")
        
    finally:
        db.close()

# Example of adding implementation for a native tool
def create_tool_implementation():
    """Create the implementation file for a native tool"""
    # Create a security_utils.py file with the password generation function
    code = """
import random
import string
from typing import Dict, Any

def generate_password(length: int = 12, include_numbers: bool = True, include_special_chars: bool = True) -> Dict[str, Any]:
    \"\"\"Generate a random password with specified length and complexity\"\"\"
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits if include_numbers else ""
    special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?" if include_special_chars else ""
    
    # Combine character sets
    all_chars = lowercase + uppercase + numbers + special_chars
    
    # Ensure at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase)
    ]
    
    if include_numbers:
        password.append(random.choice(numbers))
    
    if include_special_chars:
        password.append(random.choice(special_chars))
    
    # Fill the rest randomly
    remaining_length = length - len(password)
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the password characters
    random.shuffle(password)
    
    # Return as a dictionary
    return {
        "password": "".join(password),
        "length": length,
        "includes_numbers": include_numbers,
        "includes_special_chars": include_special_chars
    }
"""
    
    # Create the directory if it doesn't exist
    import os
    os.makedirs("app/tools", exist_ok=True)
    
    # Write the code to a file
    with open("app/tools/security_utils.py", "w") as f:
        f.write(code)
    
    print("Created implementation file: app/tools/security_utils.py")

if __name__ == "__main__":
    print("Creating tool implementation...")
    create_tool_implementation()
    
    print("\nRegistering the new tool directly...")
    register_new_tool_directly() 