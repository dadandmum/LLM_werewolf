
@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)


if "%2"=="" (
    set TYPES="*"
) else (
    set TYPES=%2
)

@echo on 

python ../scripts/analyze.py -t clean_evalution -f  %FOLDER% -a %TYPES%