#!/bin/bash

#Linux commands to create a clone of the titanonline database

#instructors.sql
cat ./share/instructors.sql | sqlite3 ./var/titanonline_clone.db

#departments.sql
cat ./share/departments.sql | sqlite3 ./var/titanonline_clone.db

#courses.sql
cat ./share/courses.sql | sqlite3 ./var/titanonline_clone.db

#droplists.sql
cat ./share/droplists.sql | sqlite3 ./var/titanonline_clone.db

#enrollments.sql
cat ./share/enrollments.sql | sqlite3 ./var/titanonline_clone.db

#waitlists.sql
cat ./share/waitlists.sql | sqlite3 ./var/titanonline_clone.db