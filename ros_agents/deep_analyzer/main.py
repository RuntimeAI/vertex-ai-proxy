import os
from .llm_client import LLMClient
from .task_analyzer import TaskAnalyzer
from .task_executor import TaskExecutor
from .answer_validator import AnswerValidator
from .recursive_reasoner import RecursiveReasoner
from .model_tester import ModelTester
from .logger import DeepAnalyzerLogger
from .vertex_client import VertexAIClient
import traceback
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


def main():
    logger = DeepAnalyzerLogger()
    logger.write_report("ANALYSIS CONFIG", """
    Models: 
    - GPT-4-mini
    - Vertex AI Text-Bison
    - Self-healing Agent
    Temperature: 0
    Max Retries: 3
    """)
    
    try:
        # Initialize OpenAI
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        llm_client = LLMClient(openai_api_key)
        vertex_client = VertexAIClient()  # No project_id required
        llm = llm_client.get_llm()
        
        task_analyzer = TaskAnalyzer(llm)
        task_executor = TaskExecutor(llm)
        answer_validator = AnswerValidator(llm)
        
        recursive_reasoner = RecursiveReasoner(
            task_analyzer,
            task_executor,
            answer_validator
        )
        
        model_tester = ModelTester(llm, recursive_reasoner)

        reasoning_test = """Assume the laws of physics on Earth. 
                        A small marble is put into a normal cup and the cup is placed upside down on a table. 
                        Someone then takes the cup without changing its orientation and puts it inside the microwave. 
                        Where is the marble now?"""

        logger.write_report("TEST SCENARIO", reasoning_test)

        # Test single run
        result = recursive_reasoner.process(reasoning_test)
        logger.write_report("SINGLE RUN RESULT", result)

        # Test multiple runs
        test_results = model_tester.test_llms(reasoning_test, 5)
        logger.write_report("MULTIPLE RUNS RESULT", str(test_results))

    except Exception as e:
        logger.log_error("main", str(e), traceback.format_exc())
        logger.write_report("ERROR", str(e))

if __name__ == "__main__":
    main()