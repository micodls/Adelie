#!/usr/bin/env bash

for dir in *; do
    if test -d "$dir"; then
        (
            cd "$dir"
            for file in *; do
                newfile=$dir.${file##*.}
                mv "$file" "$newfile"
            done
        )
    fi
done