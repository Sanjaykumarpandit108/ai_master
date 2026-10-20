import json

from openai import OpenAI
from dotenv import load_dotenv
import os

from tools import Tools, FUNCTION_NAME_TO_FUNCTION_MAPPING

load_dotenv() # it will load the environment variables from the .env file

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

messages = []

# this is system
messages.append(
    {
        "role": "system",
        "content": "You are a helpful assistant. You will answer the user's questions to the best of your ability."
    }
)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break   
    # Append the user's message to the conversation history
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=os.getenv("Model"),
        messages=messages,
        tools=Tools
    )
    #  print(f"\nRaw response: {response}")

    msg = response.choices[0].message
    if msg.tool_calls:
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            fn = FUNCTION_NAME_TO_FUNCTION_MAPPING.get(func_name)
            result = fn(**func_args) if fn else None
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result) if result is not None else "No result returned from the tool."
                }
            )

        # 2nd call to the LLM with the tool's output
        response = client.chat.completions.create(
                model=os.getenv("Model"),
                messages=messages,
            )

        msg = response.choices[0].message

    messages.append(
        {
            "role": "assistant",
            "content": msg.content
        }
    )

    print(f"\nAssistant: {msg.content}")