from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
    ToxicityMetric
)
from langchain_ollama import OllamaLLM
import time
import os
import json
from datetime import datetime
from pathlib import Path

class ResponseTimeMetric:
    def __init__(self, threshold=5.0):
        self.threshold = threshold
    
    def measure(self, time):
        return time <= self.threshold

class ModelEvaluator:
    def __init__(self, model_names=[
        "llama3.2:latest", 
        "llama3.2:1b", 
        "moondream",
        "qwen2:0.5b",
        "qwen2:1.5b",
        "gemma2:2b",
        # "mistral:latest"
    ]):
        self.model_names = model_names
        self.models = {}
        self._initialize_models()
        self.output_dir = Path("./modelEval/eval_result")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _initialize_models(self):
        for model_name in self.model_names:
            self.models[model_name] = OllamaLLM(
                model=model_name,
                temperature=0.7,
                callback_manager=None,
                verbose=True
            )
    
    def evaluate_response_time(self, prompt):
        results = {}
        metric = ResponseTimeMetric(threshold=5.0)
        
        for model_name, model in self.models.items():
            start_time = time.time()
            response = model.invoke(prompt)
            elapsed_time = time.time() - start_time
            
            results[model_name] = {
                "response": response,
                "time": elapsed_time,
                "passed": metric.measure(elapsed_time)
            }
        return results

    def evaluate_model(self, test_cases):
        evaluation_results = {}
        
        for model_name, model in self.models.items():
            metrics = {
                "relevancy": AnswerRelevancyMetric(),
                "contextual_relevancy": ContextualRelevancyMetric(),
                "faithfulness": FaithfulnessMetric(),
                "toxicity": ToxicityMetric()
            }
            
            model_results = {}
            
            for test_case in test_cases:
                response = model.invoke(test_case["prompt"])
                
                for metric_name, metric in metrics.items():
                    score = metric.measure(
                        # expected_output=response,
                        context=test_case.get("context", ""),
                        ground_truth=test_case.get("reference", "")
                    )
                    
                    if metric_name not in model_results:
                        model_results[metric_name] = []
                    model_results[metric_name].append(score)
            
            # Calculate averages for each metric
            evaluation_results[model_name] = {
                metric_name: sum(scores) / len(scores) 
                for metric_name, scores in model_results.items()
            }
        
        return evaluation_results

    def save_results(self, results, result_type):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{result_type}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        # Format the results with proper indentation
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"Results saved to: {filepath}")

def main():
    # Add this at the beginning of main() function
    os.environ["OPENAI_API_KEY"] = "dummy"  # Replace with your actual API key if needed
    
    # Extended test cases with varying lengths
    test_cases = [
        {
            "prompt": "Summarize the benefits of exercise",
            "reference": "Exercise improves physical health, mental wellbeing, and longevity.",
            "context": "Regular physical activity has numerous benefits for both body and mind..."
        },
        {
            "prompt": "Write a detailed explanation of how photosynthesis works in plants",
            "reference": "Photosynthesis is a complex process where plants convert sunlight into energy. They use chlorophyll to absorb sunlight, combine CO2 from the air with water from the soil, and produce glucose and oxygen. This process occurs in the chloroplasts and involves multiple steps including light-dependent and light-independent reactions.",
            "context": "Photosynthesis is the process by which plants and other organisms convert light energy into chemical energy. This process is crucial for life on Earth as it provides oxygen and food for most living organisms..."
        },
        {
            "prompt": "Write a short story about a magical forest (minimum 300 words)",
            "reference": "Deep within the ancient woods, where emerald leaves whispered secrets to the wind, stood a forest unlike any other. The trees here didn't just grow; they danced with the moonlight, their branches swaying to an ethereal melody only they could hear. Fireflies painted patterns in the air, spelling out ancient prophecies in golden light before dissolving into the darkness. [... story continues ...]",
            "context": "Creative writing prompt focusing on fantasy elements, world-building, and descriptive language..."
        }
    ]
    
    evaluator = ModelEvaluator()
    
    # Test response time with varying complexity
    response_time_prompts = [
        "What is the capital of France?",  # Short, factual
        "Explain the theory of relativity in simple terms",  # Medium, explanatory
        "Write a detailed analysis of the economic impacts of climate change on global agriculture in the next 50 years"  # Long, complex
    ]
    
    for prompt in response_time_prompts:
        response_times = evaluator.evaluate_response_time(prompt)
        print(f"\nResponse Time Results for prompt: {prompt[:50]}...")
        evaluator.save_results(response_times, f"response_times_{datetime.now().strftime('%H%M%S')}")
    
    # Run full evaluation
    results = evaluator.evaluate_model(test_cases)
    print("\nEvaluation Results:", results)
    evaluator.save_results(results, "evaluation_results")

if __name__ == "__main__":
    main()