import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Access denied'
        
        if not os.path.isfile(target_file):
            return f'Error: File not found'
            
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'\n[Truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING),
        },
        required=["file_path"]
    ),
)