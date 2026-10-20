import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from Utilities.utilities import log
from tools import Tools, run_tool_call



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
    user_input = input("\nSANJAY: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break   
    # Append the user's message to the conversation history
    messages.append({"role": "user", "content": user_input})


    #  print(f"\nRaw response: {response}")
    MAX_TOOL_CALLS = 10  # Set a maximum number of tool calls to prevent infinite loops
    #this is chained tool calls, where the output of one tool can be used as input for another tool
    # many times chined tool calls called the agent loop, where the agent can call tools multiple times to get the final answer
    for step in range(MAX_TOOL_CALLS):  # Limit the number of steps to avoid infinite loops


        response = client.chat.completions.create(
        model=os.getenv("Model"),
        messages=messages,
        tools=Tools
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        log(f"\nStep {step + 1}: model requestted  {len(msg.tool_calls)} tool calls detected.")

        messages.append(msg)

        for tool_call in msg.tool_calls:
            result = run_tool_call(tool_call);
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result) if result is not None else "No result returned from the tool."
                }
            )

    else: #this else block will execute if the for loop completes without a break, meaning the maximum tool calls were reached
        #we Ran out out of steps, so we will break the loop and not make any more tool calls
        fallback = "sorry, I have reached the maximum number of tool calls. Please try again with a different query."
        messages.append(
            {
                "role": "assistant",
                "content": fallback
            }
        )
        print(f"\nAssistant: {fallback}")
        continue  # Skip the rest of the loop and go back to the beginning


    messages.append(
        {
            "role": "assistant",
            "content": msg.content
        }
    )

    print(f"\nAssistant: {msg.content or 'No content returned from the assistant.'}")