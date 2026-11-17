"""
Automated pipeline execution runner script.
"""

import sys
from pathlib import Path

# Add src to pythonpath
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir / "src"))

from atmograph.cli import main

if __name__ == "__main__":
    sys.exit(main())
