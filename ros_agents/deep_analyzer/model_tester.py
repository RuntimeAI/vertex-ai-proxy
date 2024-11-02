from typing import Dict, Any
import traceback
from langchain.prompts import ChatPromptTemplate
from .logger import DeepAnalyzerLogger

class ModelTester:
    def __init__(self, llm, recursive_reasoner, vertex_client=None):
        self.llm = llm
        self.recursive_reasoner = recursive_reasoner
        self.vertex_client = vertex_client
        self.logger = DeepAnalyzerLogger()

    def test_model(self, task: str) -> str:
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You will be given a logical question, think about it and give me the final answer"),
                ("user", "The logical question is: {task}")
            ])
            
            chain = prompt | self.llm
            result = chain.invoke({"task": task})
            return result.content if hasattr(result, 'content') else str(result)
        except Exception as e:
            self.logger.log_error("test_model", str(e), task)
            return f"Error: {str(e)}"

    def correct_or_not(self, answer):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You will be given an answer to question. Your only task is to return "Correct" if the answer is about something being on a table and "Wrong" if it's anything else"""),
            ("user", "Answer : {answer}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"answer": answer})
        return result.content

    def test_llms(self, question: str, n: int) -> Dict[str, Any]:
        sdata = {}
        models_to_test = {
            "chatgpt-4o-mini": self._test_chatgpt,
            "self-healing-agent": self._test_recursive
        }
        
        if self.vertex_client:
            models_to_test["gemini-1.5-pro"] = self._test_gemini

        for model_name, test_func in models_to_test.items():
            try:
                model_stats = test_func(question, n)
                sdata[model_name] = model_stats
                
                correct_count = sum(1 for result in model_stats.values() if result == "Correct")
                accuracy = correct_count / len(model_stats)
                print(f"{model_name.capitalize()} accuracy: {accuracy:.2%}")
                
            except Exception as e:
                error_msg = f"Error in {model_name} test: {str(e)}\n{traceback.format_exc()}"
                self.logger.log_error(model_name, error_msg)
                sdata[model_name] = {"error": str(e)}

        return sdata

    def _test_chatgpt(self, question: str, n: int) -> Dict[str, str]:
        stats = {}
        for i in range(n):
            try:
                response = self.test_model(question)
                shortened_response = self.recursive_reasoner.task_executor.shorten_answer(question, response)
                verdict = self.correct_or_not(shortened_response)
                result = "Correct" if "correct" in verdict.lower() else "Wrong"
                
                self.logger.log_model_test("ChatGPT", i, shortened_response, result)
                stats[str(i)] = result
            except Exception as e:
                self.logger.log_error("ChatGPT Test", str(e), f"Test #{i}")
                stats[str(i)] = "Error"
        return stats

    def _test_recursive(self, question: str, n: int) -> Dict[str, str]:
        stats = {}
        for i in range(n):
            try:
                result = self.recursive_reasoner.process(question)
                shortened_response = self.recursive_reasoner.task_executor.shorten_answer(question, result)
                verdict = self.correct_or_not(shortened_response)
                result = "Correct" if "correct" in verdict.lower() else "Wrong"
                
                self.logger.log_model_test("Recursive Reasoner", i, shortened_response, result)
                stats[str(i)] = result
            except Exception as e:
                self.logger.log_error("Recursive Test", str(e), f"Test #{i}")
                stats[str(i)] = "Error"
        return stats

    def _test_gemini(self, question: str, n: int) -> Dict[str, str]:
        stats = {}
        for i in range(n):
            try:
                response = self.vertex_client.get_completion(question)
                shortened_response = self.recursive_reasoner.task_executor.shorten_answer(question, response)
                verdict = self.correct_or_not(shortened_response)
                result = "Correct" if "correct" in verdict.lower() else "Wrong"
                
                self.logger.log_model_test("Gemini", i, shortened_response, result)
                stats[str(i)] = result
            except Exception as e:
                self.logger.log_error("Gemini Test", str(e), f"Test #{i}")
                stats[str(i)] = "Error"
        return stats