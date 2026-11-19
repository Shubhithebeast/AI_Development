import json
import os
from datetime import datetime
import requests
from utilities.utilities import log


TOOL_FILE = os.path.join(os.path.dirname(__file__), "./files/todos.json")

def run_tool(tool_call):
        func_name = tool_call.function.name  
        func_args = {}
        
        try:
            func_args = json.loads(tool_call.function.arguments or "{}")
            log(f"Calling function {func_name} with arguments: {func_args}")
            fn = function_name_to_function_map.get(func_name)
            result = fn(**func_args)
        except Exception as e:
            result = f"Error while calling function {func_name}: {e}"
            
        log(f"  Function {func_name} returned: {result}")
        return str(result)

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weather(city):
    url = f"http://wttr.in/{city}?format=3"
    response = requests.get(url,timeout=5)
    response.raise_for_status() # Raise an exception if the request was unsuccessful
    return response.text

def get_city():
    return "Bangalore"


def load_todos():
    if not os.path.exists(TOOL_FILE):
        return []

    with open(TOOL_FILE, "r", encoding="utf-8") as file:
        todos = json.load(file)

    # purani file ke plain text tasks ko naye format mein badalta hai
    return [{"task": t, "done": False} if isinstance(t, str) else t for t in todos]


def save_todos(todos):
    with open(TOOL_FILE, "w", encoding="utf-8") as file:
        json.dump(todos, file, indent=4)


def add_todo(task):
    task = task.strip()

    if not task:
        raise ValueError("Task cannot be empty")

    todos = load_todos()
    todos.append({"task": task, "done": False})
    save_todos(todos)

    return f"Task '{task}' added successfully"


def list_todos():
    todos = load_todos()

    if not todos:
        return "No tasks found"

    return "\n".join(
        f"{idx}. [{'x' if todo['done'] else ' '}] {todo['task']}"
        for idx, todo in enumerate(todos, start=1)
    )

def complete_todo(number):
    todos = load_todos()

    if number < 1 or number > len(todos):
        raise ValueError(f"No task with number {number}")

    todos[number - 1]["done"] = True
    save_todos(todos)

    return f"Task '{todos[number - 1]['task']}' marked as completed"

TOOLS =[
    {
        "type": "function",
        "function": {
            "name" : "get_current_time",
            "description": "Returns the current date and time in the format YYYY-MM-DD HH:MM:SS",
            "parameters": {
                "type":"object", 
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function" : {
            "name" : "get_weather",
            "description": "Returns the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_city",
            "description": "Returns the current city",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_todo",
            "description": "Adds a new task to the todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to add"
                    }
                },
                "required": ["task"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_todos",
            "description": "Lists all tasks in the todo list",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_todo",
            "description": "Marks a task as completed using its number from the todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {
                        "type": "integer",
                        "description": "The task number shown in the todo list, starting from 1"
                    }
                },
                "required": ["number"]
            }
        }
    }
]

function_name_to_function_map ={
    "get_current_time": get_current_time,
    "get_weather": get_weather,
    "get_city": get_city,
    "add_todo": add_todo,
    "list_todos": list_todos,
    "complete_todo": complete_todo
}


