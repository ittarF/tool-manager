#!/usr/bin/env python
"""
Command-line interface (CLI) for registering new tools in Tool-Manager
"""
import argparse
import json
import sys
from app.database import SessionLocal
from app.models import Tool
from app.utils.embedding import generate_embedding

def register_tool(args):
    """Register a new tool based on CLI arguments"""
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if tool already exists
        existing_tool = db.query(Tool).filter(Tool.name == args.name).first()
        if existing_tool:
            print(f"Error: Tool '{args.name}' already exists in the database")
            return False
        
        # Parse parameters schema
        if args.parameters_file:
            try:
                with open(args.parameters_file, 'r') as f:
                    parameters_schema = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error: Could not parse parameters file: {str(e)}")
                return False
        else:
            parameters_schema = {}
        
        # Generate embedding
        embedding = generate_embedding(f"{args.name}: {args.description}")
        embedding_json = json.dumps(embedding)
        
        # Create the tool
        new_tool = Tool(
            name=args.name,
            description=args.description,
            parameters_schema=parameters_schema,
            is_native=args.native,
            function_path=args.function_path if args.native else None,
            endpoint_url=args.endpoint_url if not args.native else None,
            embedding=embedding_json
        )
        
        # Add and commit to the database
        db.add(new_tool)
        db.commit()
        db.refresh(new_tool)
        
        print(f"Tool '{args.name}' registered successfully!")
        print(f"ID: {new_tool.id}")
        print(f"Description: {new_tool.description}")
        if args.native:
            print(f"Function Path: {new_tool.function_path}")
        else:
            print(f"Endpoint URL: {new_tool.endpoint_url}")
        
        return True
    
    finally:
        db.close()

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="Register a new tool in Tool-Manager")
    
    parser.add_argument('--name', required=True, help="Name of the tool")
    parser.add_argument('--description', required=True, help="Description of the tool")
    parser.add_argument('--parameters-file', help="Path to a JSON file containing parameters schema")
    
    # Tool type group
    tool_type = parser.add_mutually_exclusive_group(required=True)
    tool_type.add_argument('--native', action='store_true', help="Register a native tool")
    tool_type.add_argument('--custom', action='store_true', help="Register a custom tool")
    
    # Conditional arguments
    parser.add_argument('--function-path', help="Function path for native tools (required if --native)")
    parser.add_argument('--endpoint-url', help="Endpoint URL for custom tools (required if --custom)")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.native and not args.function_path:
        parser.error("--function-path is required for native tools")
    
    if args.custom and not args.endpoint_url:
        parser.error("--endpoint-url is required for custom tools")
    
    # Set native flag based on arguments
    args.native = not args.custom
    
    # Register the tool
    success = register_tool(args)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 