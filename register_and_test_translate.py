"""
Script to register and test the translate_text tool using an external API
"""
import requests
import json
import time
from flask import Flask, request, jsonify
import threading

# Tool-Manager API endpoints
BASE_URL = "http://localhost:8000"
REGISTER_TOOL_URL = f"{BASE_URL}/tools"
TOOL_LOOKUP_URL = f"{BASE_URL}/tool_lookup"
TOOL_USAGE_URL = f"{BASE_URL}/tool_usage"

# Mock translation API
MOCK_API_PORT = 5000
MOCK_API_URL = f"http://localhost:{MOCK_API_PORT}/translate"

# Create a Flask app for the mock translation API
app = Flask(__name__)

# Basic language translation mappings (mock implementation)
TRANSLATIONS = {
    'en_to_es': {
        'hello': 'hola',
        'world': 'mundo',
        'good morning': 'buenos días',
        'thank you': 'gracias',
        'goodbye': 'adiós',
    },
    'en_to_fr': {
        'hello': 'bonjour',
        'world': 'monde',
        'good morning': 'bon matin',
        'thank you': 'merci',
        'goodbye': 'au revoir',
    },
    'en_to_de': {
        'hello': 'hallo',
        'world': 'welt',
        'good morning': 'guten morgen',
        'thank you': 'danke',
        'goodbye': 'auf wiedersehen',
    }
}

# Allow CORS by adding these headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/translate', methods=['POST', 'OPTIONS'])
def translate():
    """Mock translation API endpoint"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 200
    
    # Print the request for debugging
    print(f"Received translation request: {request.data}")
    
    try:
        data = request.json
        
        # Extract parameters
        text = data.get('text', '')
        source_language = data.get('source_language', 'en')
        target_language = data.get('target_language', 'es')
        
        # Create a language pair key
        lang_pair = f"{source_language}_to_{target_language}"
        
        # Check if we support this language pair
        if lang_pair not in TRANSLATIONS:
            return jsonify({
                "error": f"Unsupported language pair: {lang_pair}",
                "supported_pairs": list(TRANSLATIONS.keys())
            })
        
        # Convert text to lowercase for matching
        text_lower = text.lower()
        
        # Check if we know this phrase
        if text_lower in TRANSLATIONS[lang_pair]:
            translated = TRANSLATIONS[lang_pair][text_lower]
            
            # Try to match case of the original (very simplified)
            if text.isupper():
                translated = translated.upper()
            elif text[0].isupper():
                translated = translated.capitalize()
            
            return jsonify({
                "original_text": text,
                "translated_text": translated,
                "source_language": source_language,
                "target_language": target_language,
                "note": "This is a mock translation with limited vocabulary"
            })
        else:
            # For phrases we don't know, return a message
            return jsonify({
                "original_text": text,
                "translated_text": f"[Translation not available for: {text}]",
                "source_language": source_language,
                "target_language": target_language,
                "note": "This is a mock translation with limited vocabulary"
            })
    except Exception as e:
        print(f"Error processing translation request: {str(e)}")
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

def start_mock_api():
    """Start the mock translation API"""
    app.run(port=MOCK_API_PORT, host='0.0.0.0')

def register_translate_tool():
    """Register the translate_text tool as a custom external tool"""
    # Tool definition for translate_text
    translate_tool = {
        "name": "translate_text",
        "description": "Translate text from one language to another using an external translation service",
        "is_native": False,
        "endpoint_url": MOCK_API_URL,
        "parameters_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to translate"
                },
                "source_language": {
                    "type": "string",
                    "description": "The source language code (e.g., 'en', 'fr', 'es')",
                    "default": "en"
                },
                "target_language": {
                    "type": "string",
                    "description": "The target language code (e.g., 'en', 'fr', 'es')",
                    "default": "es"
                }
            },
            "required": ["text"]
        }
    }
    
    # Register the tool
    response = requests.post(REGISTER_TOOL_URL, json=translate_tool)
    
    # Print the response
    if response.status_code == 200:
        print(f"Tool '{translate_tool['name']}' registered successfully!")
        print("Tool details:", json.dumps(response.json(), indent=2))
        return True
    else:
        print(f"Error registering tool: {response.text}")
        return False

def test_translate_tool():
    """Test the translate_text tool using tool lookup and tool usage"""
    # Test tool lookup with translation-related prompt
    translation_prompt = "I need to translate 'hello' from English to Spanish"
    print(f"\nUser prompt: {translation_prompt}")
    
    lookup_response = requests.post(
        TOOL_LOOKUP_URL,
        json={"prompt": translation_prompt, "top_k": 3}
    )
    
    if lookup_response.status_code != 200:
        print(f"Error in tool lookup: {lookup_response.text}")
        return
    
    # Show found tools
    tools = lookup_response.json()["tools"]
    print(f"\nFound {len(tools)} relevant tools:")
    for i, tool in enumerate(tools):
        print(f"{i+1}. {tool['name']}: {tool['description']}")
    
    # Check if translate_text tool was found
    translate_tool_found = False
    for tool in tools:
        if tool["name"] == "translate_text":
            translate_tool_found = True
            break
    
    if not translate_tool_found:
        print("\nThe translate_text tool was not found in the top results. Testing directly...")
    
    # Execute translate_text tool
    print("\nExecuting translate_text tool...")
    translate_tool_call = {
        "tool_call": {
            "name": "translate_text",
            "parameters": {
                "text": "Hello",
                "source_language": "en",
                "target_language": "es"
            }
        }
    }
    
    # Print the request for debugging
    print(f"Sending request to {TOOL_USAGE_URL} with payload: {json.dumps(translate_tool_call)}")
    
    translate_response = requests.post(TOOL_USAGE_URL, json=translate_tool_call)
    
    # Print raw response for debugging
    print(f"Raw response: {translate_response.text}")
    
    if translate_response.status_code == 200:
        response_data = translate_response.json()
        
        # Check for errors in the response
        if "error" in response_data and response_data["error"]:
            print(f"Error from Tool-Manager: {response_data['error']}")
            return
            
        translate_result = response_data.get("result")
        
        if translate_result is None:
            print("Error: Result is None. Check the mock API and tool execution.")
            return
            
        if "error" in translate_result:
            print(f"Error from translation API: {translate_result['error']}")
        else:
            print(f"\nTranslation result:")
            print(f"Original text: {translate_result['original_text']}")
            print(f"Translated text: {translate_result['translated_text']}")
            print(f"From {translate_result['source_language']} to {translate_result['target_language']}")
            if "note" in translate_result:
                print(f"Note: {translate_result['note']}")
    else:
        print(f"Error executing translation tool: {translate_response.text}")
        return

    # Try another translation
    print("\nTrying another translation (Good morning)...")
    translate_tool_call = {
        "tool_call": {
            "name": "translate_text",
            "parameters": {
                "text": "Good morning",
                "source_language": "en",
                "target_language": "fr"
            }
        }
    }
    
    translate_response = requests.post(TOOL_USAGE_URL, json=translate_tool_call)
    
    if translate_response.status_code == 200:
        response_data = translate_response.json()
        translate_result = response_data.get("result")
        
        if translate_result is None:
            print("Error: Result is None for the second translation request")
            return
            
        if "error" in translate_result:
            print(f"Error from translation API: {translate_result['error']}")
        else:
            print(f"\nTranslation result:")
            print(f"Original text: {translate_result['original_text']}")
            print(f"Translated text: {translate_result['translated_text']}")
            print(f"From {translate_result['source_language']} to {translate_result['target_language']}")
    else:
        print(f"Error executing translation tool: {translate_response.text}")

if __name__ == "__main__":
    # Start the mock API in a separate thread
    print("Starting mock translation API...")
    api_thread = threading.Thread(target=start_mock_api, daemon=True)
    api_thread.start()
    
    # Wait a moment for the API to start
    time.sleep(2)
    
    # Register the translate tool
    print("\nRegistering translate_text tool...")
    if register_translate_tool():
        # Test the tool
        print("\nTesting translate_text tool...")
        test_translate_tool()
    
    # Keep the script running so the API thread stays alive
    print("\nPress Ctrl+C to exit")
    try:
        while api_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...") 