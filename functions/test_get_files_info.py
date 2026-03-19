import os 
from main  import get_files_info 

def run_debug_tests():
    print("get_files_info(\"calculator\",\".\"):")
    print(" Result for the current direcotry:")
    result1 = get_files_info("calculator", ".")
    print("\n".join(f" {line}" for line in result1.split("\n")))
    print("\n")

    print("get_files_info(\"calculator\", \"pkg\"):")
        