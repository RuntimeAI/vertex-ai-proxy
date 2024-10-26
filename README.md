# vertex-ai-proxy
proxy vertex ai to public access


# API Endpoints Documentation

This document provides information about the available models and endpoints for our API.

## Available Models

| Model Name | Description |
|------------|-------------|
| vertex_ai/gemini-1.5-pro | Google's Gemini 1.5 Pro model via Vertex AI |
| vertex_ai/gemini-1.5-flash | Google's Gemini 1.5 Flash model via Vertex AI |

## Demo Endpoint

You can access the API at the following demo endpoint:
```
https://vertexai.cloud.typox.ai
```


### API Endpoints

1. **Chat Completion**
   - URL: `/v1/chat/completions`
   - Method: POST
   - Description: Generate a chat completion using the specified model.

#### Request Format

```json
{
"model": "vertex_ai/gemini-1.5-pro",
"messages": [
{"role": "user", "content": "Hello, how are you?"}
],
"grounding_data": {
"web_search_queries": ["example query"],
"web_search_results": [{"url": "https://example.com", "content": "Example content"}]
    }
}
```
Note: The `grounding_data` field is optional and only used for VertexGrounding.



2. **Embeddings**
   - URL: `/v1/embeddings`
   - Method: POST
   - Description: Generate embeddings for the given input using the specified model.

3. **Model List**
   - URL: `/v1/models`
   - Method: GET
   - Description: Retrieve a list of available models.

For detailed usage instructions and request/response formats, please refer to our API documentation.



# Deploy to Cloud Run

```
gcloud auth login

gcloud config set project autogenstudio_knn3

gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

gcloud builds submit --config cloudbuild.yaml
```


## Environment Variables

- `SERVER_WORKERS`: Number of server workers (default: 4)

## Local Development

To run the application locally:

1. Install dependencies:
   ```
   poetry install
   ```

2. Run the application:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Testing

To test the deployed API, you can use the following curl command:

```
curl -X POST https://vertexai.cloud.typox.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vertex_ai/gemini-1.5-pro",
    "messages": [{"role": "user", "content": "Hello, how are you?"}]
  }'
```

