import logging

# Set up logging at the beginning of the file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable debug logging for specific libraries
logging.getLogger('langchain').setLevel(logging.DEBUG)
logging.getLogger('openai').setLevel(logging.DEBUG)
logging.getLogger('httpx').setLevel(logging.DEBUG)  # For HTTP request logging

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Custom chat template for chain-of-thoughts
COT_TEMPLATE = """The following is a conversation between a human and an AI assistant. The assistant follows a chain-of-thoughts approach, breaking down its thinking process step by step.

Current conversation:
{history}
Human: {input}
Assistant: Let me think about this step by step:"""

def create_conversation_chain():
    # Initialize the custom chat model with the new Mistral model
    chat = ChatOpenAI(
        model="ollama/mistral:latest",
        temperature=0.7,
        base_url="http://localhost:8000/v1",
        api_key="dummy-key",
        streaming=False
    )

    # Create conversation memory
    memory = ConversationBufferMemory()

    # Create the conversation chain with CoT prompt
    prompt = PromptTemplate(
        input_variables=["history", "input"], 
        template=COT_TEMPLATE
    )
    
    conversation = ConversationChain(
        llm=chat,
        memory=memory,
        prompt=prompt,
        verbose=True
    )
    
    return conversation

def main():
    conversation = create_conversation_chain()
    
    # Test cases
    questions = [
        "What are the key differences between Python and JavaScript?",
        "Can you help me solve this math problem: If a train travels 150 km in 3 hours, what's its average speed?",
        "Explain the concept of machine learning."
    ]
    
    for question in questions:
        print(f"\nHuman: {question}")
        response = conversation.predict(input=question)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()

