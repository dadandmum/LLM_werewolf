
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


if "%3"=="" (
    set TIME="1"
) else (
    set TIME=%3
)

@echo on

python ../scripts/analyze.py -t evaluate_LLM -f %FOLDER% -a %TYPES% -et %TIME%