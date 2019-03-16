#!/usr/bin/env bash

main () {
    test_log="../test.log"
    cd test/
    pytest test.py > $test_log
    if (( $? != 0 )); then
        cat $test_log
        cd ../
        exit 1
    fi
    cd ../src/
    env $(cat ../.env | xargs) python main.py > ../main.log
    cd ../
}

export -f main

nix-shell --run "main"
