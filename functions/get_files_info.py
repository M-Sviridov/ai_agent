import os

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

