import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_full = os.path.abspath(full_path)
    abs_work = os.path.abspath(working_directory)

    if not abs_full.startswith(abs_work):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", abs_full] + args,
            timeout=30, 
            capture_output=True,
            cwd=abs_work
        )
    except Exception as e:
        return (f"Error: executing Python file: {e}")

    if completed_process.returncode != 0:
        return f'Process exited with code {completed_process.returncode}'

    if len(completed_process.stdout) == 0:
        return "No output produced"


    return f'STDOUT: {completed_process.stdout.decode()}\nSTDERR: {completed_process.stderr.decode()}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python script.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python script to run, relative to the working directory.",
            ),
        },
    ),
)
