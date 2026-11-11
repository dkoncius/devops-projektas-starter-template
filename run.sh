#!/usr/bin/env bash
# Paleidimas viena komanda: ./run.sh  (sukuria .venv, įdiegia priklausomybes, startuoja)
set -euo pipefail
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
[ -f .env ] && { set -a; . ./.env; set +a; }
exec .venv/bin/flask --app app run --port "${PORT:-5001}"
