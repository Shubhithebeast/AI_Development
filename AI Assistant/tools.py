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

def add_todo(task):
    task = task.strip()
    
    if not task:
        raise ValueError("Task cannot be empty")
    
    if os.path.exists(TOOL_FILE):
        with open(TOOL_FILE, "r", encoding="utf-8") as file:
            todos = json.load(file)
    else:
        todos = []

    todos.append(task)

    with open(TOOL_FILE, "w",encoding="utf-8") as file:
        json.dump(todos, file, indent=4)

    return f"Task '{task}' added successfully"

def list_todos():
    if not os.path.exists(TOOL_FILE):
        return "No tasks found"

    with open(TOOL_FILE, "r", encoding="utf-8") as file:
        todos = json.load(file)

    if not todos:
        return "No tasks found"

    return "\n".join(f"{idx+1}. {todo}" for idx, todo in enumerate(todos))

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
    }
]

function_name_to_function_map ={
    "get_current_time": get_current_time,
    "get_weather": get_weather,
    "get_city": get_city,
    "add_todo": add_todo,
    "list_todos": list_todos
}


