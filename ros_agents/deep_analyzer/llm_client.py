from langchain_openai import ChatOpenAI

class LLMClient:
    def __init__(self, api_key, model='gpt-4o-mini', temperature=0):
        self.llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature
        )
    
    # def __init__(self, api_key, model='gpt-4o-mini', temperature=0):
    #     self.llm = ChatOpenAI(
    #         api_key=api_key,
    #         base_url="https://ai-proxy.cloud.typox.ai",
    #         # model=model,
    #         model="vertex_ai/gemini-1.5-pro",
    #         temperature=temperature
    #     )


    def get_llm(self):
        return self.llm