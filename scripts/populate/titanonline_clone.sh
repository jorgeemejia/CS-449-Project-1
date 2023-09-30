#!/bin/bash

#Linux commands to create a clone of the titanonline database

# Check if the 'var' folder exists, and create it if it doesn't as well as the nested 'log' folder
if [ ! -d "./var" ]; then
    mkdir -p "./var/log"
fi

# Execute classes.sql
cat ./share/classes.sql | sqlite3 ./var/titanonline_clone.db

# Execute courses.sql
cat ./share/courses.sql | sqlite3 ./var/titanonline_clone.db

# Execute departments.sql
cat ./share/departments.sql | sqlite3 ./var/titanonline_clone.db

# Execute droplists.sql
cat ./share/droplists.sql | sqlite3 ./var/titanonline_clone.db

# Execute enrollments.sql
cat ./share/enrollments.sql | sqlite3 ./var/titanonline_clone.db

# Execute instructors.sql
cat ./share/instructors.sql | sqlite3 ./var/titanonline_clone.db

# Execute students.sql
cat ./share/students.sql | sqlite3 ./var/titanonline_clone.db

# Execute waitlists.sql
cat ./share/waitlists.sql | sqlite3 ./var/titanonline_clone.db