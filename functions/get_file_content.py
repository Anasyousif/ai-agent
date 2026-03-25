import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        # 1. Security Check
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # 2. File Existence Check
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
            
        # 3. Read File (Notice the indentation here!)
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)
            
            # Check for truncation
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
            return content
    
    except Exception as e:
        return f"Error: {e}"
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the full content of a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to be read, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)        