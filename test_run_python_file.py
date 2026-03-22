from functions.run_python_file import run_python_file

def run_tests():
    # Test 1: Usage instructions (No args)
    print("Test 1: Run main.py (No args)")
    print(run_python_file("calculator", "main.py"))
    print("-" * 30)

    # Test 2: Actual Calculation
    print("Test 2: Run main.py with '3 + 5'")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("-" * 30)

    # Test 3: Run Internal Tests
    print("Test 3: Run tests.py")
    print(run_python_file("calculator", "tests.py"))
    print("-" * 30)

    # Test 4: Security Block (Traversal)
    print("Test 4: Out-of-bounds check")
    print(run_python_file("calculator", "../main.py"))
    print("-" * 30)

    # Test 5: Missing File
    print("Test 5: Non-existent file")
    print(run_python_file("calculator", "nonexistent.py"))
    print("-" * 30)

    # Test 6: Wrong Extension
    print("Test 6: Non-python file")
    print(run_python_file("calculator", "lorem.txt"))

if __name__ == "__main__":
    run_tests()