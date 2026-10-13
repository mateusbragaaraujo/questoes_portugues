@echo off
cd /d "%~dp0.."
python -m pip install --upgrade pyinstaller
python -m PyInstaller --noconfirm --clean scripts\questoes_portugues.spec
if errorlevel 1 (
  echo A geracao do executavel falhou.
  exit /b 1
)
echo.
echo Pronto: dist\QuestoesDePortugues.exe
