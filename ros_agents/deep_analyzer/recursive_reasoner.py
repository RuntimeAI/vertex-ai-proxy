import uuid
from .logger import DeepAnalyzerLogger

class RecursiveReasoner:
    def __init__(self, task_analyzer, task_executor, answer_validator):
        self.task_analyzer = task_analyzer
        self.task_executor = task_executor
        self.answer_validator = answer_validator
        self.logger = DeepAnalyzerLogger()

    def process(self, task, previous_answers="No Previous Answers", main_task_context="This is the main task", node_id=None):
        if node_id is None:
            node_id = str(uuid.uuid4())
            self.logger.write_report("ANALYSIS START", f"Task: {task}\nID: {node_id}")
        
        self.logger.log_task_start(task, node_id)
        task_doable = self.task_analyzer.check_complexity(task, main_task_context)
        
        self.logger.write_report("COMPLEXITY ANALYSIS", 
            f"Task: {task}\nIs Direct: {'false' in task_doable.lower()}\n")
        
        if "true" in task_doable.lower():
            task_answer = self.task_executor.perform_task(task, previous_answers, main_task_context)
            self.logger.write_report("DIRECT EXECUTION", 
                f"Task: {task}\nResult: {task_answer}")
            return task_answer
        else:
            checks = self.task_analyzer.generate_checks(task)
            self.logger.write_report("VALIDATION CHECKS", checks)
            
            sub_tasks = self.task_analyzer.generate_subtasks(task, checks)
            ordered_tasks = self.task_analyzer.order_tasks(task, sub_tasks)
            self.logger.write_report("SUBTASKS", "\n".join(ordered_tasks))
            
            full_answer = ""
            mt_context = f"Main Task Information: {task}\n{chr(10).join(ordered_tasks)}"
            
            for current in ordered_tasks:
                sub_task_id = str(uuid.uuid4())
                self.logger.write_report("SUBTASK EXECUTION", f"Starting subtask: {current}")
                temp_answer = self.process(current, full_answer, mt_context, sub_task_id)
                full_answer += f"{temp_answer}\n"
                self.logger.write_report("SUBTASK RESULT", f"Task: {current}\nResult: {temp_answer}")

            answer = self.task_executor.aggregate_answers(task, full_answer)
            self.logger.write_report("AGGREGATED ANSWER", answer)
            
            checked_answer = self.answer_validator.check_and_fix_answer(task, answer, checks)
            self.logger.write_report("VALIDATED ANSWER", checked_answer)
            
            short_answer = self.task_executor.shorten_answer(task, checked_answer)
            self.logger.write_report("FINAL ANSWER", short_answer)
            
            return short_answer