#!/usr/bin/env python3
"""Compatibility entry point for Calabash BI bootstrap."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    target = Path(__file__).resolve().with_name("calabash_bi_desktop.py")
    return subprocess.call([sys.executable, str(target), "bootstrap", *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
