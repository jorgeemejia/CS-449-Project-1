# Check if the 'var' folder exists, and create it if it doesn't as well as the nested 'log' folder
if (-not (Test-Path -Path ".\var" -PathType Container)) {
    New-Item -Path ".\var\log" -ItemType Directory
}

# Execute droplists.sql
Get-Content .\share\droplists.sql | sqlite3 .\var\titanonline_clone.db