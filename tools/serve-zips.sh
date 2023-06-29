#!/bin/bash

TOOLS_DIR="$(realpath "$(dirname "$0")")"
REPO_ROOT="$(realpath "$TOOLS_DIR"/..)"

cd "$REPO_ROOT"

n_poetry_envs=$(poetry env list | wc -l)
if [ "$n_poetry_envs" = "0" ]; then
    poetry install
fi

(
    cd tools
    poetry run python make_bundle.py
)

(
    cd dist/builds
    echo "Serving demo zips from $(pwd)"
    poetry run python ../../tools/cors_server.py 8126
)
