import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. REMOVE the duplicate/conflicting imports. 
# Keep only this one line for the toolbox:
from call_function import available_functions, call_function
from prompts import system_prompt

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
    
    # 3. Call the Model
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

    # 4. Process the Response (THE EXECUTION PHASE)
    if response.candidates and response.candidates[0].content.parts:
        function_results = []
        found_function_call = False
        
        for part in response.candidates[0].content.parts:
            if part.function_call:
                found_function_call = True
                
                # --- ACTUAL EXECUTION HAPPENS HERE ---
                function_call_result = call_function(part.function_call, verbose=args.verbose)
                
                # Validation Ceremony
                if not function_call_result.parts:
                    raise Exception("Function call returned no parts")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Function call returned no function_response")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Function call returned no response data")

                # Store the result part for later use
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        
        if not found_function_call:
            print("Response from Gemini:", response.text)
    else:
        print("Response from Gemini:", response.text)

    # 5. Verbose Output (Optional)
    if args.verbose and response.usage_metadata:
        print(f"\n[DEBUG] Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"[DEBUG] Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Hello from agent!")

if __name__ == "__main__":
    main()