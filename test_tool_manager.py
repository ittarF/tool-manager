"""
Test script to demonstrate using Tool-Manager with an LLM.
This script simulates how an LLM would interact with the Tool-Manager API.
"""

import requests
import json

# API endpoints
BASE_URL = "http://localhost:8000"
TOOL_LOOKUP_URL = f"{BASE_URL}/tool_lookup"
TOOL_USAGE_URL = f"{BASE_URL}/tool_usage"

def simulate_llm_with_tool_manager():
    """Simulate an LLM using Tool-Manager for tool discovery and execution"""
    # Step 1: User sends a prompt to the LLM
    user_prompt = "I need to know what time it is and also generate a random number between 50 and 100"
    print(f"User prompt: {user_prompt}")
    
    # Step 2: LLM sends the prompt to Tool-Manager for tool lookup
    tool_lookup_response = requests.post(
        TOOL_LOOKUP_URL,
        json={"prompt": user_prompt, "top_k": 3}
    )
    
    if tool_lookup_response.status_code != 200:
        print(f"Error in tool lookup: {tool_lookup_response.text}")
        return
    
    # Get relevant tools
    tools = tool_lookup_response.json()["tools"]
    print(f"\nFound {len(tools)} relevant tools:")
    for i, tool in enumerate(tools):
        print(f"{i+1}. {tool['name']}: {tool['description']}")
    
    # Step 3: LLM decides which tools to use and executes them
    # For this example, we'll use the first two tools (time and random number)
    
    # Execute get_current_time tool
    if tools and any(tool["name"] == "get_current_time" for tool in tools):
        print("\nExecuting get_current_time tool...")
        time_tool_call = {
            "tool_call": {
                "name": "get_current_time",
                "parameters": {}
            }
        }
        
        time_response = requests.post(TOOL_USAGE_URL, json=time_tool_call)
        
        if time_response.status_code == 200:
            time_result = time_response.json()["result"]
            print(f"Current time: {time_result['date']} {time_result['time']} {time_result['timezone']}")
        else:
            print(f"Error executing time tool: {time_response.text}")
    
    # Execute random_number tool
    if tools and any(tool["name"] == "random_number" for tool in tools):
        print("\nExecuting random_number tool...")
        random_tool_call = {
            "tool_call": {
                "name": "random_number",
                "parameters": {
                    "min_value": 50,
                    "max_value": 100
                }
            }
        }
        
        random_response = requests.post(TOOL_USAGE_URL, json=random_tool_call)
        
        if random_response.status_code == 200:
            random_result = random_response.json()["result"]
            print(f"Random number: {random_result['number']}")
        else:
            print(f"Error executing random number tool: {random_response.text}")
    
    # Step 4: LLM combines the results to respond to the user
    print("\nSimulated LLM response:")
    print("The current time is [time from tool] and your random number between 50 and 100 is [random number from tool].")

def test_weather_tool():
    """Test the new real weather tool"""
    print("\n--- Testing Real Weather Tool ---")
    
    # Test tool lookup with weather-related prompt
    weather_prompt = "What's the weather like in London?"
    print(f"User prompt: {weather_prompt}")
    
    lookup_response = requests.post(
        TOOL_LOOKUP_URL,
        json={"prompt": weather_prompt, "top_k": 3}
    )
    
    if lookup_response.status_code != 200:
        print(f"Error in tool lookup: {lookup_response.text}")
        return
    
    # Show found tools
    tools = lookup_response.json()["tools"]
    print(f"\nFound {len(tools)} relevant tools:")
    for i, tool in enumerate(tools):
        print(f"{i+1}. {tool['name']}: {tool['description']}")
    
    # Execute real_weather tool
    print("\nExecuting real_weather tool...")
    weather_tool_call = {
        "tool_call": {
            "name": "real_weather",
            "parameters": {
                "city": "London",
                "country_code": "GB"
            }
        }
    }
    
    weather_response = requests.post(TOOL_USAGE_URL, json=weather_tool_call)
    
    if weather_response.status_code == 200:
        weather_result = weather_response.json()["result"]
        if "error" in weather_result:
            print(f"Error from weather API: {weather_result['error']}")
        else:
            print(f"Weather in {weather_result['city']}, {weather_result['country']}:")
            print(f"Current temperature: {weather_result['temperature']['current']}{weather_result['temperature']['unit']}")
            print(f"Feels like: {weather_result['temperature']['apparent']}{weather_result['temperature']['unit']}")
            print(f"Weather condition: {weather_result['weather']['description']}")
            print(f"Humidity: {weather_result['humidity']['value']}{weather_result['humidity']['unit']}")
            print(f"Wind speed: {weather_result['wind']['speed']}{weather_result['wind']['speed_unit']}")
            print(f"Wind direction: {weather_result['wind']['direction']}{weather_result['wind']['direction_unit']}")
            if 'precipitation' in weather_result:
                print(f"Precipitation: {weather_result['precipitation']['value']}{weather_result['precipitation']['unit']}")
    else:
        print(f"Error executing weather tool: {weather_response.text}")

def list_all_available_tools():
    """Get all tools from the API"""
    print("\n--- Listing All Available Tools from API ---")
    
    response = requests.get(f"{BASE_URL}/tools")
    
    if response.status_code == 200:
        tools = response.json()
        print(f"Found {len(tools)} tools:")
        for i, tool in enumerate(tools):
            print(f"{i+1}. {tool['name']}: {tool['description']}")
            print(f"   Parameters: {json.dumps(tool['parameters_schema']) if tool['parameters_schema'] else 'None'}")
            print(f"   Native: {tool['is_native']}")
            if tool['is_native']:
                print(f"   Function path: {tool['function_path']}")
            print()
    else:
        print(f"Error getting tools: {response.text}")

def direct_test_weather_tool():
    """Directly test the real_weather tool without tool lookup"""
    print("\n--- Directly Testing Real Weather Tool ---")
    
    # Execute real_weather tool directly
    print("Executing real_weather tool directly...")
    weather_tool_call = {
        "tool_call": {
            "name": "real_weather",
            "parameters": {
                "city": "London",
                "country_code": "GB"
            }
        }
    }
    
    # Print the full request for debugging
    print(f"Sending request to {TOOL_USAGE_URL} with payload: {json.dumps(weather_tool_call)}")
    
    weather_response = requests.post(TOOL_USAGE_URL, json=weather_tool_call)
    
    # Print raw response for debugging
    print(f"Raw response: {weather_response.text}")
    
    if weather_response.status_code == 200:
        weather_result = weather_response.json()["result"]
        if "error" in weather_result:
            print(f"Error from weather API: {weather_result['error']}")
        else:
            print(f"Weather in {weather_result['city']}, {weather_result['country']}:")
            print(f"Current temperature: {weather_result['temperature']['current']}{weather_result['temperature']['unit']}")
            print(f"Feels like: {weather_result['temperature']['apparent']}{weather_result['temperature']['unit']}")
            print(f"Weather condition: {weather_result['weather']['description']}")
            print(f"Humidity: {weather_result['humidity']['value']}{weather_result['humidity']['unit']}")
            print(f"Wind speed: {weather_result['wind']['speed']}{weather_result['wind']['speed_unit']}")
            print(f"Wind direction: {weather_result['wind']['direction']}{weather_result['wind']['direction_unit']}")
            if 'precipitation' in weather_result:
                print(f"Precipitation: {weather_result['precipitation']['value']}{weather_result['precipitation']['unit']}")
    else:
        print(f"Error executing weather tool: {weather_response.text}")

if __name__ == "__main__":
    print("Testing Tool-Manager with simulated LLM interaction\n")
    print("Make sure the Tool-Manager API is running!\n")
    # List all available tools
    list_all_available_tools()
    # Directly test the weather tool
    direct_test_weather_tool()
    # Run standard tests
    simulate_llm_with_tool_manager()
    test_weather_tool() 