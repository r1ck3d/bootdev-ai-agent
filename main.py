import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from config import MAX_ITERATIONS
from call_function import available_functions, call_function
from prompt import system_prompt


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OpenRouter API key not set or found in .env file")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        message = response.choices[0].message
        messages.append(message)

        if not response.usage:
            raise RuntimeError("API response.usage is empty")

        if args.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        if message.tool_calls:
            for tool_call in message.tool_calls:
                # function_args = json.loads(tool_call.function.arguments or "{}")
                # print(f"Calling function: {tool_call.function.name}({function_args})")
                result_message = call_function(tool_call, args.verbose)
                if not result_message["content"]:
                    raise RuntimeError("result_message['content'] is empty")

                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")

        else:
            print("Final Response:")
            print(message.content)
            sys.exit(0)
    print(f"Maximum iterations of {MAX_ITERATIONS} reached")
    sys.exit(1)

if __name__ == "__main__":
    main()
