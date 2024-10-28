import logging
from openai import OpenAI
import requests
import sys

# Set up logging at the beginning of the file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable debug logging for specific libraries
logging.getLogger('openai').setLevel(logging.DEBUG)
logging.getLogger('httpx').setLevel(logging.DEBUG)

# Set the base URL to your local server
base_url = "http://localhost:8000"
# Set a dummy API key (it won't be used, but is required by the client)
api_key = "dummy_key"

# Create the client with a longer timeout
client = OpenAI(base_url=base_url + "/v1", 
                api_key=api_key)


def check_server_status():
    try:
        response = requests.get(f"{base_url}")  # Changed from f"{base_url}/"
        print(f"Server status: {response.status_code}")
        print(f"Server response: {response.text}")
        if response.status_code != 200:
            print("Server is not responding correctly")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)

def test_openai_compatibility():
    try:
        response = client.chat.completions.create(
            model="vertex_ai/gemini-1.5-pro",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"}
            ]
        )
        print("OpenAI Client Compatibility Test:")
        print(f"Response: {response.choices[0].message.content}")
        print(f"Usage: {response.usage}")
    except Exception as e:
        print(f"Error in OpenAI compatibility test: {str(e)}")
        print(f"Error type: {type(e)}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response content: {e.response.text}")

def test_google_search_retrieval():
    try:
        # Simplified tools structure
        response = client.chat.completions.create(
            model="vertex_ai/gemini-1.5-pro",
            messages=[
                {"role": "user", "content": "What is Bitcoin's latest price and give me the source and time"}
            ],
            tool_choice="auto",  # Add this to explicitly enable tool usage
            tools=[{"googleSearchRetrieval": {}}]
        )
        print("\nGoogle Search Retrieval Test:")
        print(f"Response: {response.choices[0].message.content}")
        print(f"Usage: {response.usage}")
        
        # Check if the tool was called
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            print("Tool was called:")
            for call in tool_calls:
                print(f"Tool: {call.function.name}")
                print(f"Arguments: {call.function.arguments}")
        else:
            print("No tool was called.")
    except Exception as e:
        print(f"Error in Google Search Retrieval test: {str(e)}")
        print(f"Error type: {type(e)}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response content: {e.response.text}")

if __name__ == "__main__":
    check_server_status()
    test_openai_compatibility()
    test_google_search_retrieval()
