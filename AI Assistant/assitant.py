import json

from tools import TOOLS, function_name_to_function_map

from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)

messages = []

messages.extend([
    {
        "role": "system",
        "content": "Act like humble agent and as a Software Development Assistant"
    },
    {
        "role": "system",
        "content": "give response in 20 words"
    }
])

while True:
    
    user_input = input("\nShubham: ") 
    
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break   
    
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools=TOOLS
    )
    
    msg = response.choices[0].message
    if msg.tool_calls:
        messages.append(msg)
        
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name  
            func_args = json.loads(tool_call.function.arguments or "{}")
            
            fn = function_name_to_function_map.get(func_name)
            result = fn(**func_args)
            
            messages.append({
                "role": "tool",
                "tool_id": tool_call.id,
                "content": str(result)
            })
            
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )
        
        msg = response.choices[0].message
            
    messages.append({
        "role": "assistant",
        "content": msg.content
    })
    
    print("Assistant Response:" , msg.content)

