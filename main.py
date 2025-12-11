import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function, available_functions

def main():
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    parser = argparse.ArgumentParser(description="AI Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY cannot be empty")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    if not response.usage_metadata:
        raise RuntimeError("usage_metadata from Gemini response is empty")

    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    resp_list = []
    for function_call in response.function_calls:
        call_function_resp = call_function(function_call, args.verbose)
        if (
            not call_function_resp.parts[0].function_response.response
            or not call_function_resp.parts
        ):
            raise Exception("empty function call result")

        if args.verbose: 
            print(f"-> {call_function_resp.parts[0].function_response.response}")

        resp_list.append(call_function_resp.parts[0])

    if not resp_list:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
    main()
