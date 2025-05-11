@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)

@echo on

python ../scripts/analyze.py -t al -f %FOLDER% -m default -a *