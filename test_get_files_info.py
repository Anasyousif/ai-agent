import os
# Inside functions/test_get_files_info.py
from functions.get_files_info import get_files_info

def run_debug_tests():
    # Test 1: Current Directory (.)
    print("get_files_info(\"calculator\", \".\"):")
    print("  Result for current directory:")
    result1 = get_files_info("calculator", ".")
    # Indent the result lines to match the requested format
    print("\n".join(f"  {line}" for line in result1.split("\n")))
    print("\n")

    # Test 2: Subdirectory (pkg)
    print("get_files_info(\"calculator\", \"pkg\"):")
    print("  Result for 'pkg' directory:")
    result2 = get_files_info("calculator", "pkg")
    print("\n".join(f"  {line}" for line in result2.split("\n")))
    print("\n")

    # Test 3: Absolute Path Security Check (/bin)
    print("get_files_info(\"calculator\", \"/bin\"):")
    print("  Result for '/bin' directory:")
    result3 = get_files_info("calculator", "/bin")
    print(f"    {result3}")
    print("\n")

    # Test 4: Directory Traversal Security Check (../)
    print("get_files_info(\"calculator\", \"../\"):")
    print("  Result for '../' directory:")
    result4 = get_files_info("calculator", "../")
    print(f"    {result4}")

if __name__ == "__main__":
    run_debug_tests()