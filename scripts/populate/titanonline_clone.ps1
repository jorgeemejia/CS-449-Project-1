# Check if the 'var' folder exists, and create it if it doesn't as well as the nested 'log' folder
if (-not (Test-Path -Path ".\var" -PathType Container)) {
    New-Item -Path ".\var\log" -ItemType Directory
}

# Execute departments.sql
Get-Content .\share\departments.sql | sqlite3 .\var\titanonline_clone.db

# Execute courses.sql
Get-Content .\share\courses.sql | sqlite3 .\var\titanonline_clone.db

# Execute instructors.sql
Get-Content .\share\instructors.sql | sqlite3 .\var\titanonline_clone.db

# Execute students.sql
Get-Content .\share\students.sql | sqlite3 .\var\titanonline_clone.db

# Execute classes.sql
Get-Content .\share\classes.sql | sqlite3 .\var\titanonline_clone.db

# Execute enrollments.sql
Get-Content .\share\enrollments.sql | sqlite3 .\var\titanonline_clone.db

# Execute waitlists.sql
Get-Content .\share\waitlists.sql | sqlite3 .\var\titanonline_clone.db

# Execute droplists.sql
Get-Content .\share\droplists.sql | sqlite3 .\var\titanonline_clone.db

# Execute users.sql
Get-Content .\share\users.sql | sqlite3 .\var\titanonline_clone.db

