#!/usr/bin/env python3
"""`python -m conformance --server /path/to/server.py` entry point."""

from .runner import main
import sys

if __name__ == "__main__":
    sys.exit(main())
