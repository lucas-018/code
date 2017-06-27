@echo off
if "%1"=="foo" goto SecondInstance
start /b %ñnx0 foo

timeout /t 10 /nobreak
pause
exit /b
:SecondInstance
echo %1
exit
