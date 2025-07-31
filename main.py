import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    if len(sys.argv)< 2:
        print ("Please provide a prompt as an argument")
        raise OSError(1)
    load_dotenv()
    prompt_tokens = 0
    response_tokens = 0

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001', contents = messages,
    )
    prompt_tokens += response.usage_metadata.prompt_token_count
    response_tokens += response.usage_metadata.candidates_token_count

    if len(sys.argv) == 3:
        if sys.argv[2] == "--verbose":
            print("User prompt:", sys.argv[1])
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")


    print(response.text)


if __name__ == "__main__":
    main()
