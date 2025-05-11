@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)

if "%2"=="" (
    set ENVS="werewolf_base"
) else (
    set ENVS=%3
)

@echo on
python ../scripts/main.py -f %FOLDER% -e %ENVS% 