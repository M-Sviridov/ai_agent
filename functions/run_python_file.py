import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_full = os.path.abspath(full_path)
    abs_work = os.path.abspath(working_directory)

    if not abs_full.startswith(abs_work):
        return print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

    if not os.path.isfile(full_path):
        return print(f'Error: File "{file_path}" not found.')

    if not file_path.endswith('.py'):
        return print(f'Error: "{file_path}" is not a Python file.')

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
        return print(f'Process exited with code {completed_process.returncode}')

    if len(completed_process.stdout) == 0:
        return print("No output produced")


    return print(f'STDOUT: {completed_process.stdout.decode()}\nSTDERR: {completed_process.stderr.decode()}')
