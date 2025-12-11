import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_full = os.path.abspath(full_path)
    abs_work = os.path.abspath(working_directory)

    if not abs_full.startswith(abs_work):
        return print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

    if not os.path.isfile(full_path):
        return print(f'Error: File not found or is not a regular file: "{file_path}"')

    try:
        with open(full_path) as f:
            content = f.read()
            if len(content) > MAX_CHARS:
                content = content[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

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
        required=["file_path"],
    ),
)

