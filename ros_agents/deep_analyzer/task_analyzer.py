from langchain.prompts import ChatPromptTemplate

class TaskAnalyzer:
    def __init__(self, llm):
        self.llm = llm

    def check_complexity(self, task, main_task):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You will be given a sub-task, and the main task for context. (Assume the sub-task is the main task if no main task is given)

            Your one and only goal is to determine if the task in hand is meant for multi-step reasoning or can be answered immediately using the information

            Here are some tips that will help you make a decision:
            
            1) Always return False if it's the main task, unless its very very obvious trivia type of question
            2) If it's not the main task, you should really be conservative in splitting it(returning False) unless you really think splitting it would give added benefits. So most times you'll end up returning True, unless obviosly its the main task, then you mostly return False
            
            Then, return True if want to split the task, else return False. 
            """),
            ("user", "SUB - Task Description: {input}  Main Task - {main_task}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"input": task, "main_task": main_task})
        return result.content

    def generate_checks(self, task):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You will be given a question. Assumming that there has been an answer generated for the question, what are the smallest number of checks
            we can have in place to make sure that the answer exactly answers the question given?

            Assume that any source of information used to retrieve the information is accurate, no need to ask for sources too.

            MAKE SURE EVERY CHECK IS UNIQUE AND THAT ONE CHECK NEVER DOES WHAT ANY OTHER CHECK DOES
            
            Return a numbered list of these checks in the form of questions that ensure that the question has been answered in a logical way
            """),
            ("user", "{input}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"input": task})
        return result.content

    def generate_subtasks(self, task, checks):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You will be given a question, and the tests to check the answer.

            Your task is to return the smallest number of tasks to do to answer the question, keeping in mind the tests.

            NO SUB-TASK SHOULD EVER BE ABOUT CHECKING ANYTHING. CHECKING WILL BE DONE IN A LATER STAGE ANYWAY.

            MAKE SURE THAT THE TASKS ARE CLEAR AND INSTRUCTIVE Step-by-step manner AND NEVER EVER VAGUE.
            """),
            ("user", "task : {task}, checks : {checks}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"task": task, "checks": checks})
        return result.content

    def order_tasks(self, task, sub_tasks):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You will be given a task and list of sub-tasks related to that one task
            
            You have three goals:
            First Goal - Order the list such that it follows how a normal human would do these set of tasks
            Second Goal - Remove any tasks that are duplicated
            Third Goal - Ensure that the tasks contain reference to the results of other tasks wherever needed

            Return only and ONLY a numbered list of the sub-tasks
            """),
            ("user", "task : {task}, sub_tasks : {sub_tasks}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"task": task, "sub_tasks": sub_tasks})
        return result.content.split('\n')