import os

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_full = os.path.abspath(full_path)
    abs_file = os.path.abspath(file_path)
    abs_work = os.path.abspath(working_directory)
    parent_dir = os.path.dirname(abs_file)

    if not abs_full.startswith(abs_work):
        return print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    with open(abs_file, "w") as f:
        f.write(content)
        return print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
