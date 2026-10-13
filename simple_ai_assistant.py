from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() # it will load the environment variables from the .env file

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

messages = []

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break   
    # Append the user's message to the conversation history
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=os.getenv("Model"),
        messages=messages
    )
    messages.append(
        {
            "role": "assistant",
            "content": response.choices[0].message.content
        }
    )

    print("llm response:")
    # print(response)
    print("Assistant:", response.choices[0].message.content)