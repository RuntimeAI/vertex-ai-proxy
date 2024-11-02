from langchain.prompts import ChatPromptTemplate

class TaskExecutor:
    def __init__(self, llm):
        self.llm = llm

    def perform_task(self, task, previous_answers="No Previous Answers", main_task_context="This is the main task"):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a logical genius. You will be given a simple sub-task to do, a reference to the parent task and trustable data context. Your task is to do the sub-task and sub-task only, use any other information only for reference.

            MAKE SURE YOU ARE ONLY AND ONLY PERFORMING THE SUB TASK GIVEN TO YOU, BUT IN THE CONTEXT OF THE MAIN TASK
            """),
            ("user", "SUB-TASK to do: {input}\nMain Context: {main_task_context}\nPrevious Answers: {previous_answers}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({
            "input": task,
            "main_task_context": main_task_context,
            "previous_answers": previous_answers
        })
        return result.content

    def aggregate_answers(self, task, answers):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You will be given a task and an aggregated answer which is the summation of a bunch of sub-tasks created from the task.

            Your only task is to consider the answers for all the subtasks and return the final answer
            """),
            ("user", "task : {task}, full_answer : {answers}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"task": task, "answers": answers})
        return result.content

    def shorten_answer(self, test, answer):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You'll be given the description of a task and it's final confirmed answer. Your only goal is to return only the main answer without any extra words.
            NEVER EVER SAY DATA IS NOT ENOUGH. I WANT YOU TO GIVE ONE WORD ANSWERS UNLESS YOU ABSOLUTELY NEED TO INCLUDE MORE WORDS.
            """),
            ("user", "Main Task : {task}, \n\n Answer : {answer}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"task": test, "answer": answer})
        return result.content