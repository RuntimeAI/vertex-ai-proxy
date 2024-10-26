from fastapi import FastAPI, Request
from litellm import completion
import os
import yaml
from google.auth import default
from google.auth.transport.requests import Request as GoogleRequest

app = FastAPI()

# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Set up Vertex AI settings
os.environ["VERTEX_PROJECT"] = config["general_settings"]["vertex_project"]
os.environ["VERTEX_LOCATION"] = config["general_settings"]["vertex_location"]

# Get default credentials
credentials, project = default()

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    json_data = await request.json()
    messages = json_data.get("messages", [])
    model = json_data.get("model", "vertex_ai/gemini-1.5-pro")

    # Refresh credentials if necessary
    if credentials.expired:
        credentials.refresh(GoogleRequest())

    response = completion(
        model=model,
        messages=messages,
        temperature=0.7,
        credentials=credentials
    )

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
