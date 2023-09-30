#!/bin/bash

# Check if the 'var' folder exists, and create it if it doesn't as well as the nested 'log' folder
if [ ! -d "./var" ]; then
    mkdir -p "./var/log"
fi

# Execute droplists.sql
cat ./share/droplists.sql | sqlite3 ./var/titanonline_clone.db