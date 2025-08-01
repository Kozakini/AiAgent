import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Change the content of the file with the given input",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file user wants the content to change",
            ),
            "file_content": types.Schema(
                type=types.Type.STRING,
                description="the given input of the user, the string that should be a new content of the file"
            )
        },
    ),
)
def write_file(working_directory, file_path, file_content):
    file_path = os.path.join(os.path.abspath(working_directory), file_path)
    if os.path.abspath(working_directory)  not in os.path.abspath(file_path):
        return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    try:
        f = open(file_path, "w")
        f.write(file_content)
    except Exception as e: return (f"Error: {e}")
    return f'Successfully wrote to "{file_path}" ({len(file_content)} characters written)'
