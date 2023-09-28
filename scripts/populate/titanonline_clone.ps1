# Execute instructors.sql
Get-Content .\share\instructors.sql | sqlite3 .\var\titanonline_clone.db

# Execute departments.sql
Get-Content .\share\departments.sql | sqlite3 .\var\titanonline_clone.db

# Execute courses.sql
Get-Content .\share\courses.sql | sqlite3 .\var\titanonline_clone.db

# Execute droplists.sql
Get-Content .\share\droplists.sql | sqlite3 .\var\titanonline_clone.db

# Execute enrollments.sql
Get-Content .\share\enrollments.sql | sqlite3 .\var\titanonline_clone.db

# Execute waitlists.sql
Get-Content .\share\waitlists.sql | sqlite3 .\var\titanonline_clone.db