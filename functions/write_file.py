import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return "Error: Permission denied"

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING),
            "content": types.Schema(type=types.Type.STRING),
        },
        required=["file_path", "content"]
    ),
)