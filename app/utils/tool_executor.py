import importlib
import requests
from typing import Dict, Any, Optional, Tuple

def execute_native_tool(function_path: str, parameters: Dict[str, Any]) -> Tuple[Any, Optional[str]]:
    """
    Execute a native tool by importing the function and calling it with parameters
    Returns a tuple of (result, error_message)
    """
    try:
        # Split the function path into module path and function name
        module_path, function_name = function_path.rsplit('.', 1)
        
        # Import the module
        module = importlib.import_module(module_path)
        
        # Get the function
        function = getattr(module, function_name)
        
        # Call the function with parameters
        result = function(**parameters)
        
        return result, None
    except Exception as e:
        return None, str(e)

def execute_custom_tool(endpoint_url: str, parameters: Dict[str, Any]) -> Tuple[Any, Optional[str]]:
    """
    Execute a custom tool by making an HTTP request to the endpoint URL
    Returns a tuple of (result, error_message)
    """
    try:
        print(f"Executing custom tool with endpoint: {endpoint_url}")
        print(f"Parameters: {parameters}")
        
        # Make the request to the endpoint with proper headers
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Make the request to the endpoint
        response = requests.post(
            endpoint_url, 
            json=parameters, 
            headers=headers,
            timeout=10  # Add a timeout
        )
        
        # Print response details for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text[:500]}...")  # Limit to first 500 chars
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Return the response JSON
        return response.json(), None
    except requests.exceptions.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        print(error_msg)
        # Try to include response content in the error if available
        if hasattr(e, 'response') and e.response:
            error_msg += f" - Response: {e.response.text}"
        return None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(error_msg)
        return None, error_msg

def execute_tool(tool_name: str, 
                 parameters: Dict[str, Any], 
                 is_native: bool, 
                 function_path: Optional[str] = None, 
                 endpoint_url: Optional[str] = None) -> Tuple[Any, Optional[str]]:
    """
    Execute a tool based on its type (native or custom)
    Returns a tuple of (result, error_message)
    """
    print(f"Executing tool: {tool_name}")
    print(f"Is native: {is_native}")
    print(f"Function path: {function_path}")
    print(f"Endpoint URL: {endpoint_url}")
    print(f"Parameters: {parameters}")
    
    if is_native and function_path:
        return execute_native_tool(function_path, parameters)
    elif not is_native and endpoint_url:
        return execute_custom_tool(endpoint_url, parameters)
    else:
        error_msg = f"Invalid tool configuration for {tool_name}"
        print(error_msg)
        return None, error_msg 