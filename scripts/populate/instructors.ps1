# Check if the 'var' folder exists, and create it if it doesn't as well as the nested 'log' folder
if (-not (Test-Path -Path ".\var" -PathType Container)) {
    New-Item -Path ".\var\log" -ItemType Directory
}

# Execute instructors.sql
Get-Content .\share\instructors.sql | sqlite3 .\var\titanonline_clone.db