#!/usr/bin/env bash

set -e

main () {
    set -e
    for f in $(find . -type f -name "*.py"); do
        if (( $time < $(stat -c %Y $f) )); then
            echo "linting $f"
            lint $f
        fi
    done
    pytest src/test/
    python_with .env src/main.py
}

export -f main
timestamp=".time"

if [ ! -e $timestamp ]; then
    time=0
else
    time=$(cat $timestamp)
fi

if [ -z $NIX_SHELL ]; then
    nix-shell --run main
else
    main
fi

echo $(date +%s) > $timestamp
