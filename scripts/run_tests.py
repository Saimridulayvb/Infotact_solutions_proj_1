"""
Test execution runner script for AtmoGraph.
"""

import subprocess
import sys
from pathlib import Path

def main():
    root = Path(__file__).parent.parent
    cmd = [sys.executable, "-m", "pytest", "tests"]
    print("Running AtmoGraph automated test suite...")
    res = subprocess.run(cmd, cwd=root)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
