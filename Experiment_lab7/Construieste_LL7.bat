@echo off
setlocal
cd /d "%~dp0"
set "PY=py -3"
where py >nul 2>nul
if errorlevel 1 set "PY=python"
%PY% construieste.py
if errorlevel 1 goto eroare
if /i not "%~1"=="--fara-pauza" pause
exit /b 0
:eroare
echo Construirea a esuat. Verifica mesajul de mai sus.
if /i not "%~1"=="--fara-pauza" pause
exit /b 1
