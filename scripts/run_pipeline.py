"""
Automated pipeline execution runner script.
Profiles execution duration and forwards exit code.
"""

import sys
import time
from pathlib import Path

# Add src to pythonpath
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir / "src"))

from atmograph.cli import main

if __name__ == "__main__":
    start_t = time.time()
    code = main()
    elapsed = time.time() - start_t
    print(f"Pipeline execution finished in {elapsed:.2f}s (exit code {code})")
    sys.exit(code)
