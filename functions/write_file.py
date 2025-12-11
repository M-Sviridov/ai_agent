import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_full = os.path.abspath(full_path)
    abs_file = os.path.abspath(file_path)
    abs_work = os.path.abspath(working_directory)
    parent_dir = os.path.dirname(abs_file)

    if not abs_full.startswith(abs_work):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    try:
        with open(abs_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to file: {e}"

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
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)
