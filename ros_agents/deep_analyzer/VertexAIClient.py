from vertexai.language_models import ChatModel
import vertexai

class VertexAIClient:
    def __init__(self, project_id, location="us-central1"):
        vertexai.init(project=project_id, location=location)
        self.chat_model = ChatModel.from_pretrained("gemini-1.5-pro")
        self.chat = self.chat_model.start_chat()

    def get_completion(self, prompt):
        response = self.chat.send_message(prompt)
        return response.text