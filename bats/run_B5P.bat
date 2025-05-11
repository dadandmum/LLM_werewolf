
@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)

python ../scripts/main_mul.py -e werewolf_B5P_Check -f  %FOLDER% -c 1