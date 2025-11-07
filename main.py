import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from constants import *
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    if len(sys.argv)< 2:
        print ("Please provide a prompt as an argument")
        raise OSError(1)
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ],
    )
    load_dotenv()
    prompt_tokens = 0
    response_tokens = 0


    if len(sys.argv) == 3:
            if sys.argv[2] == "--verbose":
                print("User prompt:", sys.argv[1])
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")



    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]
    for i in range(0, 20):
        response = client.models.generate_content(
            model = 'gemini-2.0-flash-001', contents = messages,
            config = types.GenerateContentConfig(
                tools=[available_functions], system_instruction = system_prompt
            )
        )


        if response.candidates:
            for canditate in response.candidates:
                messages.append(canditate.content)



        prompt_tokens += response.usage_metadata.prompt_token_count
        response_tokens += response.usage_metadata.candidates_token_count


        if response.function_calls is not None:
            for function in response.function_calls:
                responded = types.Content(
                    role="tool",
                    parts=[
                            types.Part.from_function_response(
                            name= function.name,
                            response = {"result": call_function(function)},
                        )
                    ]
                )
                messages.append(responded)

        if not response.function_calls:
            if response.text:
                print(f"Final response:\n{response.text}")
                break


if __name__ == "__main__":
    main()
