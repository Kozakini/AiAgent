import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file that the user wants to get the content of",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    file_path = os.path.join(os.path.abspath(working_directory), file_path)
    if os.path.abspath(working_directory)  not in os.path.abspath(file_path):
        return (f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(file_path):
        return (f'Error: "{file_path}" is not a file')
    try:
        f = open(file_path, "r")
        if len(str(f)) > 10000:
            file_content = f.read(10000) + f"...File {file_path} truncated at 10000 characters"
        else:
            file_content = f.read(10000)
    except Exception as e: return (f"Error: {e}")
    return file_content
