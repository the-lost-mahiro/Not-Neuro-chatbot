"""Resolve local data files independently of the working directory."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
