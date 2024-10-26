# vertex-ai-proxy
proxy vertex ai to public access


# API Endpoints Documentation

This document provides information about the available models and endpoints for our API.

## Available Models

| Model Name | Description |
|------------|-------------|
| vertex_ai/gemini-1.5-pro | Google's Gemini 1.5 Pro model via Vertex AI |

## Demo Endpoint

You can access the API at the following demo endpoint:
```
https://vertexai.cloud.typox.ai
```


### Endpoints

1. **Chat Completion**
   - URL: `/v1/chat/completions`
   - Method: POST
   - Description: Generate a chat completion using the specified model.

2. **Embeddings**
   - URL: `/v1/embeddings`
   - Method: POST
   - Description: Generate embeddings for the given input using the specified model.

3. **Model List**
   - URL: `/v1/models`
   - Method: GET
   - Description: Retrieve a list of available models.

For detailed usage instructions and request/response formats, please refer to our API documentation.

ENV VARS
```
SERVER_WORKERS=4
```

