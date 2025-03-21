# Tool Registration Guide

This document explains how to register new tools in the Tool-Manager system.

## Types of Tools

The Tool-Manager supports two types of tools:

1. **Native Tools**: Implemented directly within the application using Python functions.
2. **Custom Tools**: External tools accessed via API endpoints.

## Registration Methods

There are three ways to register new tools:

### 1. Using the API

The simplest way to register a tool is by making a POST request to the `/tools` endpoint:

```bash
curl -X POST http://localhost:8000/tools \
  -H "Content-Type: application/json" \
  -d '{
    "name": "translate_text",
    "description": "Translate text from one language to another",
    "is_native": false,
    "endpoint_url": "https://api.example-translation.com/translate",
    "parameters_schema": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string",
          "description": "The text to translate"
        },
        "target_language": {
          "type": "string",
          "description": "The target language code"
        }
      },
      "required": ["text", "target_language"]
    }
  }'
```

You can also use the provided `register_tool_example.py` script:

```bash
python register_tool_example.py
```

### 2. Using Python Code Directly

For more control, you can use Python code to register tools, especially useful for native tools with implementations:

```bash
python register_tool_directly.py
```

This script:
1. Creates a new tool implementation (a password generator)
2. Registers the tool in the database

### 3. Using the Command-Line Interface

For quick registration, use the CLI tool:

```bash
# Register a native tool
python register_tool_cli.py --name "search_web" \
  --description "Search the web for information" \
  --native \
  --function-path "app.tools.web_utils.search_web" \
  --parameters-file example_parameters.json

# Register a custom tool
python register_tool_cli.py --name "analyze_image" \
  --description "Analyze an image using computer vision" \
  --custom \
  --endpoint-url "https://api.vision-service.com/analyze" \
  --parameters-file example_parameters.json
```

## Parameters Schema Format

The parameters schema follows the JSON Schema format. Here's an example:

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The search query"
    },
    "max_results": {
      "type": "integer",
      "description": "Maximum number of results to return",
      "default": 10
    }
  },
  "required": ["query"]
}
```

Save this as a JSON file to use with the CLI tool, or include it directly in the API request or Python code.

## Creating Native Tool Implementations

Native tools require an implementation. Create a Python function with the following characteristics:

1. Located in a module that can be imported (e.g., `app.tools.my_module.my_function`)
2. Accepts parameters as defined in the parameters schema
3. Returns a dictionary with the results
4. Has proper type hints and docstrings

Example:

```python
def my_tool(param1: str, param2: int = 10) -> Dict[str, Any]:
    """Tool description here"""
    # Implementation
    result = do_something(param1, param2)
    return {"result": result, "other_info": "additional data"}
```

After creating the function, register it using one of the methods above. 