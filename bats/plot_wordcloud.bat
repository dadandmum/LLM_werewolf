@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)


if "%2"=="" (
    set SESSION="none"
) else (
    set SESSION=%2
)

@echo on

python ../scripts/gen_wc.py -f %FOLDER% -s %SESSION%