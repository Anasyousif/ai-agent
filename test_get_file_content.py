from functions.get_file_content import get_file_content

def run_tests():
    # 1. Test Truncation
    print("Testing Truncation (lorem.txt):")
    res_lorem = get_file_content("calculator", "lorem.txt")
    print(f"  Length: {len(res_lorem)}")
    print(f"  Ends with: {res_lorem[-60:]}\n")

    # 2. Test main.py - PRINT THE WHOLE THING or at least 500 chars
    print("Testing main.py:")
    print(get_file_content("calculator", "main.py")) 
    print("\n")

    # 3. Test pkg/calculator.py - PRINT THE WHOLE THING
    print("Testing pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("\n")

    # 4. Test Security
    print("Testing Security (/bin/cat):")
    print(get_file_content("calculator", "/bin/cat"))
    print("\n")

    # 5. Test Missing File
    print("Testing Missing File:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    run_tests()