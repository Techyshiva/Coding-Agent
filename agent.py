# Chain Of Thought Prompting
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional
import requests

import time
import json
import os

load_dotenv()

client = OpenAI(
    api_key="AIzaSyCqMdV79Nc0L5L3nrHuZulrMt1Pn8_Ywqg",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

import subprocess

def run_comand(cmd: str):
    # Execute the command and capture the terminal output
    result = subprocess.getoutput(cmd)
    
    # If the command worked but produced no text (like 'mkdir'), give the AI a thumbs up
    if result.strip() == "":
        return f"Command '{cmd}' executed successfully with no output."
    
    return result

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return f"Something went wrong"

def write_file(json_input_str: str):
    try:
        # Parse the JSON string provided by the AI
        data = json.loads(json_input_str)
        filepath = data.get("path")
        content = data.get("content")
        
        # Create the folder if it doesn't exist yet
        folder = os.path.dirname(filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)
            
        # Write the beautifully formatted multi-line code to the file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Successfully wrote multi-line code to {filepath}"
    except Exception as e:
        return f"Failed to write file. Error: {str(e)}"

available_tools = {
    "get_weather": get_weather,
    "run_comand": run_comand,
    "write_file": write_file
}


SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call an tool if required from the list of available tools
    For every tool call wait for the observe step which is the output from the called tool

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).
    - for codes like HTML CSS JS. you can go in multiple planning steps to create Efficient Code files.
    - Don't Create Code Text as one line. Keep it, as it is written by a developer itself in multiple lines. 

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL, "content": "string", "tool":" "string", "input": "string"}
    
    Available tools: 
    - get_weather(city: str): Takes city name as an input string and returns the weather information about the city
    - run_comand(cmd: str): Takes a system Windows Command as string and executes the command on users system and reutrns the output from that command
    - write_file(json_input_str: str): Takes a JSON string with "path" and "content" keys. Use this to create or overwrite files with beautifully formatted, multi-line code.

    Example 1:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN", "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN", "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN", "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT", "content": "3.5" }
    
    Example 2  :
    START: What is the weather of Delhi
    PLAN: { "step": "PLAN", "content": "I need to call get_weather for Delhi" }
    PLAN: { "step": "TOOL", "tool": "get_weather", "input": "delhi" }
    PLAN: { "step": "OBSERVE", "tool": "get_weather", "Output": "The temperature of delhi is cloudy with 20 C" }
    OUTPUT: { "step": "OUTPUT", "content": "The Current weather in Delhi is 20 Degree Celcius with some Cloudy Sky" }
    
    Example 3:
    START: Create a simple HTML file named index.html
    PLAN: { "step": "PLAN", "content": "I need to write multi-line HTML code to index.html using the write_file tool" }
    PLAN: { "step": "TOOL", "tool": "write_file", "input": "{\"path\": \"index.html\", \"content\": \"<!DOCTYPE html>\\n<html>\\n<head>\\n  <title>App</title>\\n</head>\\n<body>\\n  <h1>Hello</h1>\\n</body>\\n</html>\"}" }
    OUTPUT: { "step": "OUTPUT", "content": "I have successfully created the index.html file with formatted code." }
"""


class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description = "The ID of the tool to call")
    input: Optional[str] = Field(None, description="The imput Params for the tool")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    print("\n" + "="*50 + "\n") # Just a visual separator
    user_query = input("👉🏻 (Enter your Prompt OR type 'exit' to quit): ")
    
    # Allow the user to stop the script gracefully
    if user_query.lower() in ['exit', 'quit']:
        print("Stopping agent...")
        break

    message_history.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.parse(
            model="gemini-3.1-flash-lite-preview",
            response_format=MyOutputFormat,
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})
        
        parsed_result = response.choices[0].message.parsed
        
        # Safeguard: If the LLM returns a list, extract the first dictionary
        if isinstance(parsed_result, list):
            if len(parsed_result) > 0:
                parsed_result = parsed_result[0]
            else:
                continue # Skip empty lists gracefully

        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue
        
        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"🛠️ {tool_to_call} ({tool_input})")
            
            tool_response = available_tools[tool_to_call](tool_input)
            message_history.append({"role": "user", "content": json.dumps(
                {"step": "OBSERVE", "tool": tool_to_call,"input": tool_input, "output": tool_response}
            )  })
            continue

        if parsed_result.step == "PLAN":
            print("🧠", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("🤖", parsed_result.content)
            break
        
        if parsed_result.step not in ["START", "PLAN", "TOOL", "OUTPUT"]:
            print(f"⚠️ Agent confused. It returned unknown step: {parsed_result.step}")
            break
        
        time.sleep(1)
        
        print("\n")

print("\n\n\n")