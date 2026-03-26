import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" outside working directory'

        files = os.listdir(target_dir)
        result = [f"{f} | {os.path.getsize(os.path.join(target_dir, f))} bytes | {'Directory' if os.path.isdir(os.path.join(target_dir, f)) else 'File'}" for f in files]
        return "\n".join(result) if result else "Directory is empty"
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(type=types.Type.STRING),
        },
    ),
)