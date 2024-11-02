import requests
import json

def test_google_search_retrieval():
    url = "http://localhost:8000/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer dummy_key"
    }
    # Update the tools format to match OpenAI's function calling format
    payload = {
        "model": "vertex_ai/claude-3-sonnet",
        "messages": [
            {"role": "user", "content": "What are the latest developments in quantum computing?"}
        ],
        "tools": [
        {
            "googleSearchRetrieval": {} 
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        print("Google Search Retrieval Test:")
        print(f"Response: {result['choices'][0]['message']['content']}")
        print(f"Usage: {result['usage']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_google_search_retrieval()
