
@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)
@echo on 

python ../scripts/analyze.py -t analyze_vote -f  %FOLDER% -m default