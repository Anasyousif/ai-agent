import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import our system prompt and our toolbox
from prompts import system_prompt
from call_function import available_functions

load_dotenv()

def main():
    # 1. Setup CLI arguments
    parser = argparse.ArgumentParser(description="AI Coding Agent")
    parser.add_argument("user_prompt", type=str, help="The question or task for the agent")
    parser.add_argument("--verbose", action="store_true", help="Show token usage and debug info")
    args = parser.parse_args()

    # 2. Initialize the Gemini Client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")
    
    client = genai.Client(api_key=api_key)
    
    # 3. Call the Model with Tools and System Instructions
    # Note: Using gemini-2.5-flash which is the stable standard for 2026
    model_id = "gemini-2.5-flash"

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=[args.user_prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                temperature=0
            )
        )
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return

    # 4. Process the Response
    # Check if the AI wants to call a function or just talk
    if response.candidates and response.candidates[0].content.parts:
        found_function_call = False
        
        for part in response.candidates[0].content.parts:
            if part.function_call:
                found_function_call = True
                # Format: Calling function: name({'arg': 'val'})
                print(f"Calling function: {part.function_call.name}({part.function_call.args})")
        
        # If no function calls were found in the parts, print the text response
        if not found_function_call:
            print("Response from Gemini:", response.text)
    else:
        # Fallback for empty responses
        print("Response from Gemini:", response.text)

    # 5. Verbose Output (Optional)
    if args.verbose and response.usage_metadata:
        print(f"\n[DEBUG] Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"[DEBUG] Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Hello from agent!")

if __name__ == "__main__":
    main()