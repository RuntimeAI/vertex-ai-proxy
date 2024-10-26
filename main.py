from fastapi import FastAPI, Request, HTTPException
from litellm import completion
import os
import yaml
from google.auth import default
from google.auth.transport.requests import Request as GoogleRequest
from typing import Optional
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
import time

app = FastAPI()

# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Set up Vertex AI settings
os.environ["VERTEX_PROJECT"] = config["general_settings"]["vertex_project"]
os.environ["VERTEX_LOCATION"] = config["general_settings"]["vertex_location"]

# Set up Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Get default credentials
credentials, _ = default()

@observe(as_type="generation")
def vertex_completion(**kwargs):
    start_time = time.time()
    
    # Extract relevant fields from kwargs
    messages = kwargs.pop('messages', [])
    model = kwargs.pop('model', 'vertex_ai/gemini-1.5-pro')
    grounding_data = kwargs.pop('grounding_data', None)
    
    # Update Langfuse context
    langfuse_context.update_current_observation(
        input=messages,
        model=model,
        metadata={
            "grounding_data": str(grounding_data) if grounding_data else "None",
            **kwargs
        }
    )
    
    # Refresh credentials if necessary
    if credentials.expired:
        credentials.refresh(GoogleRequest())
    
    # Set the appropriate generative model
    generative_model = "gemini-1.5-pro"
    
    response = completion(
        model=model,
        messages=messages,
        temperature=0.7,
        credentials=credentials,
        grounding_data=grounding_data,
        generative_model=generative_model
    )
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Update Langfuse context with usage information
    langfuse_context.update_current_observation(
        output=response['choices'][0]['message']['content'],
        usage={
            "prompt_tokens": response['usage']['prompt_tokens'],
            "completion_tokens": response['usage']['completion_tokens'],
            "total_tokens": response['usage']['total_tokens']
        },
        metadata={"processing_time": processing_time}
    )
    
    return response

@app.post("/v1/chat/completions")
@observe(as_type="vertex_ai_proxy")
async def chat_completions(request: Request):
    try:
        json_data = await request.json()
        return vertex_completion(**json_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
