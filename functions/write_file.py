import os
from google.genai import types
def write_file(working_directory, file_path, content):
    try:
        # 1. Define target_file at the very top
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        # 2. Security Check
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # 3. Directory Check
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # 4. Create directories if they don't exist
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        # 5. Write the file
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a specified file, creating directories if necessary",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path where the file should be written, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file",
            ),
        },
        required=["file_path", "content"]
    ),
)        