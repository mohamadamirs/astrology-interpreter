#!/usr/bin/env bash
# Script Pengujian Otomatis Astrology-Interpreter
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${PROJECT_ROOT}"

echo "🧪 Menjalankan Astrology-Interpreter Benchmark Test Suite..."
/root/.venvs/astrology/bin/python -m pytest -v "${PROJECT_ROOT}/backend/tests" "$@"
