#!/usr/bin/env bash

main () {
    cd test/
    pytest test.py
    if (( $? == 0 )); then
        cd ../src/
        env $(cat ../.env | xargs) python main.py
    fi
    cd ../
}

export -f main

nix-shell --run "main"
