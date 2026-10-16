"""Generate the frontend category contract; --check detects stale generated data."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from error_types import ErrorType

path = Path(__file__).resolve().parents[2] / 'frontend/src/data/errorTypes.json'
expected = json.dumps([item.value for item in ErrorType], indent=2) + '\n'
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
if parser.parse_args().check:
    if not path.exists() or path.read_text() != expected:
        raise SystemExit('Frontend error types are stale. Run scripts/export_error_types.py.')
else:
    path.write_text(expected)
