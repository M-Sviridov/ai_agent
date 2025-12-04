import os
import argparse
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY cannot be empty")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    args = parser.parse_args()

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=args.prompt
    )

    if not response.usage_metadata:
        raise RuntimeError("usage_metadata from Gemini response is empty")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
