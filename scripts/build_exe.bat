@echo off
setlocal

REM Build Windows executable for Desktop Pet
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pyinstaller --noconfirm --clean desktop_pet.spec

echo.
echo Build complete.
echo EXE path: dist\DesktopPet.exe
endlocal
