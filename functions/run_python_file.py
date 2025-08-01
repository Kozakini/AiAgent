from posix import wait
import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the inputed by the user python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file user wants to run, first argument",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description='Extra arguments for the program, for example calc program needs 2 arguments: python3 calc "3 + 5" etc.'
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    file_pathy = os.path.join(os.path.abspath(working_directory), file_path)
    if os.path.abspath(working_directory)  not in os.path.abspath(file_pathy):
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(file_pathy):
        return (f'Error: File "{file_path}" not found')
    if not file_path.endswith(".py"):
        return (f'Error: "{file_path}" is not a Python file')
    try:
        completed_process = subprocess.run(["python3", file_pathy, *args], capture_output = True, timeout = 30, cwd = working_directory)
    except Exception as e: return (f"Error: executing Python file: {e}")
    process_code = ""
    stdout = f"STDOUT:\n{completed_process.stdout.decode()}"
    stderr = f"STDERR:\n{completed_process.stderr.decode()}"
    if completed_process.returncode != 0:
        process_code = f"\nProcess exited with code {completed_process.returncode}"
    if not completed_process.stdout and not completed_process.stderr:
        return ("No output produced.")
    return (f"{stdout}{stderr}{process_code}")
