#!/bin/bash

TOOLS_DIR="$(realpath "$(dirname "$0")")"
REPO_ROOT="$(realpath "$TOOLS_DIR"/..)"

cd "$REPO_ROOT"

n_poetry_envs=$(poetry env list | wc -l)
if [ "$n_poetry_envs" = "0" ]; then
    poetry install
fi

python3 "$TOOLS_DIR"/make_bundle.py

cd "$REPO_ROOT/dist/builds"
echo "Serving demo zips from $(pwd)"
exec python3 "$TOOLS_DIR"/cors_server.py 8126
