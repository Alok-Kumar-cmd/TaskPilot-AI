
import json
import os

from groq import Groq
from dotenv import load_dotenv

from tools import (
    calculate,
    add_task,
    list_tasks,
    complete_task,
    knowledge_search
)


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError("GROQ_API_KEY is missing.")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"

# -----------------------------
# TOOL DEFINITIONS
# -----------------------------

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the user's task list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string"
                    }
                },
                "required": ["description"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Show all tasks stored by the user.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed using its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string"
                    }
                },
                "required": ["task_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "knowledge_search",
            "description": "Search the local AI knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string"
                    }
                },
                "required": ["topic"]
            }
        }
    }
]


# -----------------------------
# TOOL EXECUTION
# -----------------------------

def execute_tool(name, arguments):

    function_map = {
        "calculate": calculate,
        "add_task": add_task,
        "list_tasks": list_tasks,
        "complete_task": complete_task,
        "knowledge_search": knowledge_search
    }

    if name not in function_map:
        return {"error": "Unknown tool"}

    try:
        result = function_map[name](**arguments)
        return result

    except Exception as e:
        return {"error": str(e)}


# -----------------------------
# AI AGENT
# -----------------------------

def run_agent(user_input, history=None):

    messages = [
        {
            "role": "system",
            "content": """
            You are TaskPilot, an intelligent AI assistant.

            You can:
            1. Perform calculations.
            2. Manage user tasks.
            3. Search the local knowledge base.
            4. Answer general questions.

            Rules:
            - Use tools whenever they are useful.
            - Never claim a task was added or completed without
              successfully executing the corresponding tool.
            - Ask for clarification if a task ID is ambiguous.
            - Be friendly, concise and helpful.
            - Do not invent tool results.
            """
        }
    ]

    if history:
        messages.extend(history[-10:])

    messages.append({
        "role": "user",
        "content": user_input
    })

    # Agent reasoning and tool execution loop

    for step in range(5):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2
        )

        message = response.choices[0].message

        # No tool required: return final answer

        if not message.tool_calls:

            return message.content or "I couldn't generate a response."

        # Add assistant's tool call to conversation

        assistant_message = {
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": []
        }

        for call in message.tool_calls:

            assistant_message["tool_calls"].append({
                "id": call.id,
                "type": "function",
                "function": {
                    "name": call.function.name,
                    "arguments": call.function.arguments
                }
            })

        messages.append(assistant_message)

        # Execute selected tools

        for call in message.tool_calls:

            name = call.function.name
            arguments = json.loads(call.function.arguments)

            result = execute_tool(name, arguments)

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "name": name,
                "content": json.dumps(result)
            })

    return "I reached the maximum number of tool execution steps."
