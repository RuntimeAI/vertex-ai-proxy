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

You can test the Vertex AI Proxy using curl commands. Here are some examples:

### 1. Basic Gemini-1.5-pro with Temperature Adjustment

```
bash
curl -X POST https://ai-proxy.cloud.typox.ai/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
"model": "vertex_ai/gemini-1.5-pro",
"messages": [
{"role": "user", "content": "Generate a creative story about a time-traveling scientist in exactly 50 words."}
],
"temperature": 0.9
}'
```
This request uses the Gemini-1.5-pro model with a higher temperature (0.9) for more creative outputs.

### 2. Gemini-1.5-flash Multi-turn Conversation
```
bash
curl -X POST https://ai-proxy.cloud.typox.ai/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
"model": "vertex_ai/gemini-1.5-flash",
"messages": [
{"role": "user", "content": "I want to learn a new programming language. What do you suggest?"},
{"role": "assistant", "content": "Great! There are many programming languages to choose from. To give you the best suggestion, could you tell me more about your goals? Are you interested in web development, data science, mobile apps, or something else?"},
{"role": "user", "content": "I'm interested in data science and machine learning."}
]
}'
```

This request demonstrates a multi-turn conversation using the Gemini-1.5-flash model, which is optimized for faster responses.

### 3. Grounding Example
```
bash
curl -X POST https://ai-proxy.cloud.typox.ai/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
"model": "vertex_ai/gemini-1.5-pro",
"messages": [
{"role": "user", "content": "Based on the weather data provided, what activities would you recommend for today?"}
],
"grounding_data": {
"location": "San Francisco",
"date": "2024-03-15",
"temperature": "68°F",
"conditions": "Partly cloudy",
"wind_speed": "10 mph"
}
}'
```


This request uses grounding data to provide context-specific information to the model, allowing for more accurate and relevant responses.

## Deployment

The project includes a `cloudbuild.yaml` file for easy deployment to Google Cloud Run. Make sure to set up your Google Cloud project and enable necessary APIs before deployment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)


