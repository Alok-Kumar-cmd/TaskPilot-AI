
import ast
import json
import operator
import os
import uuid

TASK_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


# -----------------------------
# 1. Safe Calculator
# -----------------------------

def calculate(expression):

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    def evaluate(node):

        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Exponent too large")

            return allowed_operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.operand))

        raise ValueError("Unsupported mathematical expression")

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree)

        if isinstance(result, (int, float)) and abs(result) > 1e100:
            return "Result too large"

        return result

    except Exception as e:
        return f"Calculation error: {str(e)}"


# -----------------------------
# 2. Task Storage
# -----------------------------

def load_tasks():

    if not os.path.exists(TASK_FILE):
        return []

    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):

    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


# -----------------------------
# 3. Add Task
# -----------------------------

def add_task(description):

    tasks = load_tasks()

    task = {
        "id": str(uuid.uuid4())[:8],
        "description": description,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)

    return task


# -----------------------------
# 4. List Tasks
# -----------------------------

def list_tasks():

    tasks = load_tasks()

    if not tasks:
        return "You have no tasks."

    return tasks


# -----------------------------
# 5. Complete Task
# -----------------------------

def complete_task(task_id):

    tasks = load_tasks()

    for task in tasks:

        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)

            return f"Task {task_id} completed successfully."

    return "Task ID not found."


# -----------------------------
# 6. Knowledge Tool
# -----------------------------

def knowledge_search(topic):

    knowledge = {
        "python": "Python is a high-level programming language used in AI, ML, automation and web development.",
        "machine learning": "Machine Learning enables computers to learn patterns from data and make predictions.",
        "artificial intelligence": "Artificial Intelligence is the field of creating systems capable of performing tasks that typically require human intelligence.",
        "rag": "Retrieval Augmented Generation combines information retrieval with LLM generation to provide context-grounded answers.",
        "agentic ai": "Agentic AI systems can reason about tasks, select tools, execute actions and use results to complete objectives."
    }

    topic = topic.lower().strip()

    for key, value in knowledge.items():

        if key in topic:
            return value

    return "No matching topic in the local knowledge base."
