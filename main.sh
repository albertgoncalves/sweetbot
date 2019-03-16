#!/usr/bin/env bash

main () {
    set -e
    for f in $(find . -type f -name "*.py"); do
        echo $f
        flake8_ignore $f
    done
    pytest
    python_with .env src/main.py
}

export -f main

nix-shell --run "main"
