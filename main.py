from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from litellm import completion
import os
import yaml
from google.auth import default
from google.auth.transport.requests import Request as GoogleRequest
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

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

class ChatCompletionRequest(BaseModel):
    model: str = Field(default="vertex_ai/gemini-1.5-pro")
    messages: List[Dict[str, str]]
    temperature: Optional[float] = 0.7
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[str] = None
    stream: Optional[bool] = False

    class Config:
        extra = "allow"

@observe(as_type="generation")
def vertex_completion(model: str, messages: List[Dict[str, str]], 
                     temperature: float = 0.7, tools: Optional[List[Dict[str, Any]]] = None, 
                     **kwargs):
    try:
        # Refresh credentials if necessary
        if credentials.expired:
            credentials.refresh(GoogleRequest())

        # Call completion with explicit parameters
        completion_args = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "credentials": credentials,
        }
        
        if tools:
            completion_args["tools"] = tools
            
        response = completion(**completion_args)
        
        # Update Langfuse with response data
        langfuse_context.update_current_observation(
            output=response['choices'][0]['message']['content'],
            usage=response['usage']
        )
        
        return response
        
    except Exception as e:
        print(f"Error in vertex_completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
@observe(as_type="vertex_ai_proxy")
async def chat_completions(request: ChatCompletionRequest):
    try:
        # Log incoming request
        print(f"Received request: {request.model_dump()}")
        
        # Extract and standardize parameters
        completion_args = {
            "model": request.model,
            "messages": request.messages,
            "temperature": request.temperature,
        }
        
        # Only add tools if they're present
        if request.tools:
            completion_args["tools"] = request.tools
            
        if request.tool_choice:
            completion_args["tool_choice"] = request.tool_choice

        # Call vertex_completion with standardized parameters
        response = vertex_completion(**completion_args)
        
        # Ensure response matches OpenAI format
        if isinstance(response, dict):
            response.setdefault("model", request.model)
            response.setdefault("object", "chat.completion")
            
            if "choices" in response:
                for choice in response["choices"]:
                    choice.setdefault("finish_reason", "stop")
                    if "message" in choice:
                        choice["message"].setdefault("role", "assistant")
        
        return response
        
    except Exception as e:
        print(f"Error in chat_completions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Vertex AI Proxy is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        workers=config["general_settings"].get("server_workers", 4)
    )
