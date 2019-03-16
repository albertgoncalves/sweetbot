#!/usr/bin/env bash

for d in "__pycache__" ".pytest_cache"; do
    echo "deleting $d"
    find . -name $d -type d -prune -exec rm -r {} \;
done
