@echo off
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Stopping running instances...
taskkill /F /IM MediaFloat.exe 2>nul

echo Building MediaFloat...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

pyinstaller FloatControl.spec --noconfirm --clean

echo.
echo Build complete! The executable is in the 'dist' folder.
pause