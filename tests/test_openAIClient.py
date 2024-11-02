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

# Create the client
client = OpenAI(base_url=base_url + "/v1", api_key=api_key)

def check_server_status():
    try:
        response = requests.get(f"{base_url}")
        print(f"Server status: {response.status_code}")
        print(f"Server response: {response.text}")
        if response.status_code != 200:
            print("Server is not responding correctly")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)

def test_gemini_pro_model():
    try:
        response = client.chat.completions.create(
            model="vertex_ai/gemini-1.5-pro",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of Germany?"}
            ]
        )
        print("Gemini Pro Model Test:")
        print(f"Response: {response['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"Error in Gemini Pro model test: {str(e)}")

if __name__ == "__main__":
    check_server_status()
    test_gemini_pro_model()
    # test_mistral_model()
