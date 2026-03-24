import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # 1. Path Standardization
        abs_working_dir = os.path.abspath(working_directory)
        # If no directory provided, use the working directory
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        # 2. Security Check: Is it inside the 'fence'?
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # 3. Existence Check
        if not os.path.exists(target_dir):
            return f'Error: Directory "{directory}" does not exist'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # 4. List Files
        files = os.listdir(target_dir)
        result = []
        for file in files:
            path = os.path.join(target_dir, file)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            # Format each line: name | size | directory status
            result.append(f"{file} | {size} bytes | {'Directory' if is_dir else 'File'}")

        return "\n".join(result) if result else "Directory is empty"

    except Exception as e:
        return f"Error: {e}"

# --- SCHEMA DEFINITION (MUST BE UNINDENTED) ---
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)