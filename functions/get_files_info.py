import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Get information about files in a directory and their size and if they are directories",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory to get information about",
            ),
        },
    ),
)
def get_files_info(working_directory, directory = "."):
    directory = os.path.join(os.path.abspath(working_directory), directory)
    if os.path.abspath(working_directory)  not in os.path.abspath(directory):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(directory):
        return (f'Error: "{directory}" is not a directory')
    return_statment = ""
    try:
        for file in os.listdir(directory):
                 return_statment += (
                f"{file}: file_size={os.path.getsize(os.path.join(directory, file))}"+
                f" bytes, is_dir={os.path.isdir(os.path.join(directory, file))}\n"
            )
    except Exception as e: return (f"Error: {e}")
    return (return_statment)

