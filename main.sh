#!/usr/bin/env bash

main () {
    set -e
    for f in */*py; do
        flake8_ignore $f
    done
    pytest
    python_with .env main.py
}

export -f main

nix-shell --run "main"
