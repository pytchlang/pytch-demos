#!/bin/bash

TOOLS_DIR="$(realpath "$(dirname "$0")")"
REPO_ROOT="$(realpath "$TOOLS_DIR"/..)"

if [ -r "$TOOLS_DIR"/venv/bin/activate ]; then
    source "$TOOLS_DIR"/venv/bin/activate
else
    cd "$TOOLS_DIR"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

python3 "$TOOLS_DIR"/make_bundle.py

cd "$REPO_ROOT/dist/components"
echo "Serving demo zips from $(pwd)"
exec python3 "$TOOLS_DIR"/cors_server.py 8126
