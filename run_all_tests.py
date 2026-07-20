import subprocess
import sys

def main():
    print("========================================")
    print("STARTING END-TO-END SYSTEM TESTS")
    print("========================================\n")
    
    print("Running Pytest Suite (NLP & API Integration)...")
    result = subprocess.run([sys.executable, "-m", "pytest", "backend/"], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
        
    if result.returncode == 0:
        print("ALL BACKEND TESTS PASSED SUCCESSFULLY!\n")
    else:
        print("SOME TESTS FAILED! Please review the output above.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
