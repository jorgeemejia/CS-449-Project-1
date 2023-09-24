# Execute instructors.sql
Get-Content .\share\instructors.sql | sqlite3 .\var\titanonline_clone.db

# Execute departments.sql
Get-Content .\share\departments.sql | sqlite3 .\var\titanonline_clone.db