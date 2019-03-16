#!/usr/bin/env bash

if [ $(uname -s) = "Darwin" ]; then
    alias ls='ls --color=auto'
    alias ll='ls -al'
fi

flake8_ignore () {
    flake8 --ignore "E124,E128,E201,E203,E241,E402,W503,E722"
}

python_creds () {
    env $(cat .env | xargs) python $1
}

export -f flake8_ignore
export -f python_creds
