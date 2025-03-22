# Tool Manager API Documentation

This document provides comprehensive information about the Tool Manager API endpoints, request formats, and response structures.

## Base URL

All API endpoints are relative to the base URL of your Tool Manager instance: `http://your-server:8000`

## Authentication

Currently, Tool Manager does not implement authentication. All endpoints are publicly accessible.

## API Endpoints

### Tool Management

#### List All Tools

```
GET /tools
```

Returns a list of all registered tools.

**Response:**
```json
[
  {
    "id": 1,
    "name": "tool_name",
    "description": "Tool description",
    "parameters_schema": {},
    "is_native": true,
    "function_path": "app.tools.function_name",
    "endpoint_url": null,
    "parameters": []
  },
  ...
]
```

#### Get Tool by ID

```
GET /tools/{tool_id}
```

Returns details for a specific tool.

**Parameters:**
- `tool_id` (path parameter, integer): The ID of the tool to retrieve

**Response:**
```json
{
  "id": 1,
  "name": "tool_name",
  "description": "Tool description",
  "parameters_schema": {},
  "is_native": true,
  "function_path": "app.tools.function_name",
  "endpoint_url": null,
  "parameters": []
}
```

#### Create Tool

```
POST /tools
```

Register a new tool.

**Request Body:**
```json
{
  "name": "new_tool_name",
  "description": "Description of what the tool does",
  "parameters_schema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "Description of parameter 1"
      },
      "param2": {
        "type": "string",
        "description": "Description of parameter 2"
      }
    },
    "required": ["param1"]
  },
  "is_native": true,
  "function_path": "app.tools.my_function",
  "endpoint_url": null
}
```

**Notes:**
- For native tools (is_native=true), provide the function_path
- For external tools (is_native=false), provide the endpoint_url

**Response:**
The newly created tool object with its assigned ID.

#### Update Tool

```
PUT /tools/{tool_id}
```

Update an existing tool.

**Parameters:**
- `tool_id` (path parameter, integer): The ID of the tool to update

**Request Body:**
```json
{
  "name": "updated_tool_name",
  "description": "Updated description",
  "parameters_schema": {}
}
```

**Response:**
The updated tool object.

#### Delete Tool

```
DELETE /tools/{tool_id}
```

Delete a tool.

**Parameters:**
- `tool_id` (path parameter, integer): The ID of the tool to delete

**Response:**
```json
{
  "message": "Tool 'tool_name' deleted successfully"
}
```

### Tool Lookup

#### Find Relevant Tools

```
POST /tool_lookup
```

Find tools relevant to a user prompt using embedding similarity.

**Request Body:**
```json
{
  "prompt": "I need to translate text from English to Spanish",
  "top_k": 3
}
```

**Parameters:**
- `prompt` (string, required): The user prompt to match against tool descriptions
- `top_k` (integer, optional, default=3): Number of most relevant tools to return

**Response:**
```json
{
  "tools": [
    {
      "name": "translate_text",
      "description": "Translates text between languages",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "description": "Text to translate"
          },
          "source_language": {
            "type": "string",
            "description": "Source language code"
          },
          "target_language": {
            "type": "string",
            "description": "Target language code"
          }
        },
        "required": ["text", "target_language"]
      }
    },
    ...
  ]
}
```

### Tool Usage

#### Execute Tool

```
POST /tool_usage
```

Execute a tool call and return the result.

**Request Body:**
```json
{
  "tool_call": {
    "name": "translate_text",
    "parameters": {
      "text": "Hello world",
      "source_language": "en",
      "target_language": "es"
    }
  }
}
```

**Response:**
```json
{
  "result": "Hola mundo",
  "error": null
}
```

If an error occurs:
```json
{
  "result": null,
  "error": "Error message describing what went wrong"
}
```

## Data Models

### Tool

A tool represents a function that can be executed, either natively or via an external API endpoint.

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| name | string | Unique name for the tool |
| description | string | Description of what the tool does |
| parameters_schema | object | JSON Schema defining tool parameters |
| is_native | boolean | Whether the tool is implemented natively |
| function_path | string | Path to native function (for native tools) |
| endpoint_url | string | URL for external API (for external tools) |

### Parameter

Metadata about a tool parameter.

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| tool_id | integer | ID of the tool this parameter belongs to |
| name | string | Parameter name |
| description | string | Parameter description |
| parameter_type | string | Data type of the parameter |
| required | boolean | Whether the parameter is required |

## External Tool Integration

External tools can be integrated by:

1. Creating an API endpoint that accepts POST requests with JSON parameters
2. Registering the tool with the parameters:
   - `is_native`: Set to `false`
   - `endpoint_url`: URL to your API endpoint

The external tool should return a JSON response with the result of the operation.

## Error Handling

The API returns standard HTTP status codes:

- 200: Successful operation
- 400: Bad request (invalid parameters)
- 404: Resource not found
- 500: Server error

Error responses include a detail message:

```json
{
  "detail": "Error message"
}
```

## Examples

### Registering a Native Tool

```bash
curl -X POST http://localhost:8000/tools -H "Content-Type: application/json" -d '{
  "name": "format_text",
  "description": "Formats text according to specified style",
  "parameters_schema": {
    "type": "object",
    "properties": {
      "text": {
        "type": "string",
        "description": "Text to format"
      },
      "style": {
        "type": "string",
        "description": "Style to apply (bold, italic, etc.)",
        "enum": ["bold", "italic", "underline", "code"]
      }
    },
    "required": ["text", "style"]
  },
  "is_native": true,
  "function_path": "app.tools.text.format_text"
}'
```

### Registering an External Tool

```bash
curl -X POST http://localhost:8000/tools -H "Content-Type: application/json" -d '{
  "name": "weather_forecast",
  "description": "Get weather forecast for a location",
  "parameters_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name or coordinates"
      },
      "days": {
        "type": "integer",
        "description": "Number of days to forecast",
        "default": 1
      }
    },
    "required": ["location"]
  },
  "is_native": false,
  "endpoint_url": "https://your-weather-api.example.com/forecast"
}'
```

### Executing a Tool

```bash
curl -X POST http://localhost:8000/tool_usage -H "Content-Type: application/json" -d '{
  "tool_call": {
    "name": "format_text",
    "parameters": {
      "text": "Hello world",
      "style": "bold"
    }
  }
}'
``` 