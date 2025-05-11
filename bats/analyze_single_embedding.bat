
@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)
python ../scripts/analyze.py -t single_embedding -s werewolf_base_2024-08-03-14-43-39 -f %FOLDER% -m default