from langchain.prompts import ChatPromptTemplate

class AnswerValidator:
    def __init__(self, llm):
        self.llm = llm

    def check_answer(self, task, answer, check):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You will be given a task, the answer to the task and a specific thing to check about the answer.
            Assume all sources of the data are perfectly accurate and up to date
            Return True if the answer meets the check, if not return false
            """),
            ("user", "task : {task}, answer : {answers}, check : {check}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"task": task, "answers": answer, "check": check})
        return result.content

    def fix_answer(self, task, answer, check):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You will be given the description of a task, it's answer and a test that the answer failed. 
            Your task is to return the correct answer that actually passes the test
            """),
            ("user", "Main Task : {task}, Answer : {answer}, Test that the answer failed : {check}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"task": task, "answer": answer, "check": check})
        return result.content

    def check_and_fix_answer(self, task, initial_answer, checks, max_retries=3):
        current_answer = initial_answer
        failed_tasks = checks.split('\n')
        retry_count = 0
        
        while failed_tasks and retry_count < max_retries:
            new_failed_tasks = []
            
            for current_check in failed_tasks:
                answer_check = self.check_answer(task, current_answer, current_check)
                if "False" in answer_check.lower():
                    new_failed_tasks.append(current_check)

            if not new_failed_tasks:
                return current_answer
            
            for failed_check in new_failed_tasks:
                current_answer = self.fix_answer(task, current_answer, failed_check)
            
            failed_tasks = new_failed_tasks
            retry_count += 1

        return current_answer