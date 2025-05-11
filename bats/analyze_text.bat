
@echo off

if "%1"=="" (
    set FOLDER="temp"
) else (
    set FOLDER=%1
)
@echo on 
python ../scripts/analyze.py -t multiple_embedding -f %FOLDER% -m default