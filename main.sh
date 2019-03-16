#!/usr/bin/env bash

main () {
    set -e
    for f in */*py; do flake8_ignore $f; done
    cd test/
    pytest
    if (( $? == 0 )); then
        cd ../
        python_creds main.py
    fi
}

export -f main

nix-shell --run "main"

