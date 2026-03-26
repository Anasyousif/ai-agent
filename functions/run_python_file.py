import subprocess
import os
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        # 1. Path Setup
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # 2. Security Check
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" outside working directory'

        # 3. Execution
        # We use python3 to ensure we are in the correct environment
        cmd = ["python3", target_file]
        if args:
            cmd.extend(args)

        # The Key: capture_output=True grabs both stdout and stderr
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=abs_working_dir
        )

        # Combine both streams so the "Ran 9 tests" string is caught
        combined_output = result.stdout + result.stderr
        
        if not combined_output:
            return "Execution finished with no output."
            
        return combined_output

    except Exception as e:
        return f"Error executing script: {e}"

# --- SCHEMA DEFINITION ---
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
                description="Optional list of command-line arguments",
            ),
        },
        required=["file_path"]
    ),
)