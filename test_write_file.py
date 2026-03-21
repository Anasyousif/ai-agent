from functions.write_file import write_file

def run_tests():
    # Test 1: Overwriting an existing file
    print("Test 1: Overwrite existing file")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print("\n")

    # Test 2: Creating a new file in a subdirectory
    print("Test 2: Create file in subdirectory")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print("\n")

    # Test 3: Security Breach (Should fail)
    print("Test 3: Attempt out-of-bounds write")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

if __name__ == "__main__":
    run_tests()