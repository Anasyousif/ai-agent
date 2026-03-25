import os
from google.genai import types
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        # 1. Path Standardization
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        # 2. Security Check
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # 3. Existence & File Type Check
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
            
        # 4. Extension Check
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
            
        # 5. Build the Command
        command = ["python", target_file]
        if args:
            command.extend(args)
            
        # 6. Execute via Subprocess
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 7. Format the Output String
        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
            
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")
                
        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: execution timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the .py file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the script",
            ),
        },
        required=["file_path"]
    ),
)        