@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)

if "%2"=="" (
    set COUNT=1
) else (
    set COUNT=%2
)


if "%3"=="" (
    set ENVS="werewolf_base"
) else (
    set ENVS=%3
)

@echo on
python ../scripts/main_mul.py -f %FOLDER% -c %COUNT% -e %ENVS% 