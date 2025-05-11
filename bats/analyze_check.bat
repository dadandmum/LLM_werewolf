@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)
if "%2"=="" (
    set CHECK_TYPE="*"
) else (
    set CHECK_TYPE=%2
)
@echo on

python ../scripts/analyze.py -t cv -f %FOLDER% -c %CHECK_TYPE%