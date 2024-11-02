import logging
import os
from datetime import datetime

class DeepAnalyzerLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"deep_analyzer_{timestamp}.log")
        self.report_file = os.path.join(log_dir, f"analysis_report_{timestamp}.txt")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("DeepAnalyzer")
        
    def write_report(self, section, content):
        with open(self.report_file, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"{section}\n")
            f.write(f"{'='*50}\n")
            f.write(f"{content}\n")
    
    def log_task_start(self, task, node_id=None):
        self.logger.info(f"Starting task processing - ID: {node_id} - Task: {task}")
    
    def log_complexity_check(self, task, is_complex):
        self.logger.info(f"Complexity check for task: {task} - Is complex: {is_complex}")
    
    def log_subtasks_generation(self, subtasks):
        self.logger.info(f"Generated subtasks: {subtasks}")
    
    def log_checks_generation(self, checks):
        self.logger.info(f"Generated validation checks: {checks}")
    
    def log_task_execution(self, task, result):
        self.logger.info(f"Task execution - Task: {task} - Result: {result}")
    
    def log_validation(self, task, original_answer, validated_answer):
        self.logger.info(f"Answer validation - Task: {task}")
        self.logger.info(f"Original answer: {original_answer}")
        self.logger.info(f"Validated answer: {validated_answer}")
    
    def log_error(self, component, error_message, context=None):
        error_log = f"Error in {component}: {error_message}"
        if context:
            error_log += f"\nContext: {context}"
        self.logger.error(error_log)
    
    def log_model_test(self, model_name, test_number, response, verdict):
        self.logger.info(f"Model Test - {model_name} - Test #{test_number}")
        self.logger.info(f"Response: {response}")
        self.logger.info(f"Verdict: {verdict}")