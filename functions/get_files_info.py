import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to list its content from, relative to the working directory.",
            ),
        },
    ),
)

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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write or overwrite, relative to the working directory.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_full = os.path.abspath(full_path)
    abs_work = os.path.abspath(working_directory)

    if not abs_full.startswith(abs_work):
        return print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

    if not os.path.isdir(abs_work):
        return print(f'Error: "{directory}" is not a directory')

    dir_contents = os.listdir(full_path)
    contents = []
    for content in dir_contents:
        path = os.path.join(full_path, content)
        contents.append(f"- {content}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}")

    return print("\n".join(contents))
