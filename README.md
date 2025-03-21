# Tool-Manager

A FastAPI application designed to store tool information and implementations, with support for both native and external tools.

## Features

- Tool information storage in a database
- Native tool implementations through FastAPI
- External tool integration via HTTP endpoints
- Tool lookup using embedding similarity
- Tool usage via standard JSON LLM interaction format

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python run.py
   ```
   
   Or manually with:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `POST /tool_lookup`: Find relevant tools based on user prompt
- `POST /tool_usage`: Execute a tool call and return the response
- `GET /tools`: List all available tools
- `POST /tools`: Register a new tool
- `GET /tools/{tool_id}`: Get tool details by ID
- `PUT /tools/{tool_id}`: Update an existing tool
- `DELETE /tools/{tool_id}`: Delete a tool

## External Tool Integration

Tool-Manager supports integration with external tools via HTTP endpoints. To register an external tool:

1. Create an API endpoint that accepts POST requests with JSON parameters
2. Register the tool with Tool-Manager by specifying:
   - `name`: A unique name for the tool
   - `description`: Tool description for LLM context
   - `parameters_schema`: JSON schema defining the tool's parameters
   - `is_native`: Set to `false` for external tools
   - `endpoint_url`: The URL of your tool's API endpoint
   - `parameters`: Optional array of parameter metadata

### External Tool Response Format

External tools should return a JSON response. The structure can be as simple as:

```json
{
  "result": "value"
}
```

Or more detailed:

```json
{
  "result_field1": "value1",
  "result_field2": "value2",
  "note": "Optional note about the execution"
}
```

### Example: Registering an External Tool

Here's a template for registering an external tool:

```bash
curl -X POST http://localhost:8000/tools -H "Content-Type: application/json" -d '{
  "name": "your_tool_name",
  "description": "Description of what your tool does",
  "parameters_schema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "Description of parameter 1"
      },
      "param2": {
        "type": "string",
        "description": "Description of parameter 2",
        "default": "default_value"
      }
    },
    "required": ["param1"]
  },
  "is_native": false,
  "endpoint_url": "http://your-api-endpoint/path",
  "parameters": []
}'
```

## Testing Tools

You can test registered tools using the `/tool_usage` endpoint:

```bash
curl -X POST http://localhost:8000/tool_usage -H "Content-Type: application/json" -d '{
  "tool_call": {
    "name": "your_tool_name",
    "parameters": {
      "param1": "value1",
      "param2": "value2"
    }
  }
}'