#!/usr/bin/env python3
"""Run all tests in this directory without requiring pytest.

None of these tests call OpenAI or need OPENAI_API_KEY -- they use only
synthetic, runtime-generated images.

Usage: python3 tests/run_all.py
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(Path(__file__).resolve().parent), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
