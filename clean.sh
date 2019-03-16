#!/usr/bin/env bash

for d in "__pycache__" ".pytest_cache"; do
    find . -type d -name $d -exec rm -ri {} \;
done
