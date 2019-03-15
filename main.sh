#!/usr/bin/env bash

main () {
    cd src/
    env $(cat ../.env | xargs) python main.py > ../log
    cd ../
}

export -f main

nix-shell --run "main"
