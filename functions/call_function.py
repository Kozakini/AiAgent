import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai  import types

def call_function(function_call_part, verbose=False):
    if verbose:
          print(f"- Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"- Calling function: {function_call_part.name}")

    function_response = ""
    match function_call_part.name:
        case "get_files_info":
            function_response = get_files_info("./calculator", **function_call_part.args)
        case "get_file_content":
            function_response = get_file_content("./calculator", **function_call_part.args)
        case "run_python_file":
            function_response = run_python_file("./calculator", **function_call_part.args)
        case "write_file":
            function_response = write_file("./calculator", **function_call_part.args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name= function_call_part.name,
                        response={"error": f"Function {function_call_part.name} not found"},
                    )
                ],
            )
    return function_response
