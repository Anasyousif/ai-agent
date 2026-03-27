import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", type=str)
    args = parser.parse_args()

    # FORCE CHECK: If .env fails, try to get it from the shell environment
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env or shell.")
        return

    client = genai.Client(api_key=api_key)
    
    # Starting the conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Use 1.5-flash for the best tool-calling stability in this environment
    model_id = "gemini-1.5-flash"

    for i in range(20):
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
                    temperature=0 # Keep it precise for debugging
                )
            )
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return

        if response.candidates:
            messages.append(response.candidates[0].content)

        tool_results = []
        parts = response.candidates[0].content.parts if response.candidates else []
        
        for part in parts:
            if part.function_call:
                # The agent will likely call 'get_files_info' then 'get_file_content'
                # and finally 'write_file' to fix the bug.
                res = call_function(part.function_call)
                tool_results.append(res.parts[0])

        if not tool_results:
            print("\n--- Agent Task Complete ---")
            print(response.text)
            break
        else:
            messages.append(types.Content(role="user", parts=tool_results))

if __name__ == "__main__":
    main()