@echo off
echo ==========================================
echo  Instalador de Calculadora ET0
echo  Instalando dependencias de Python...
echo ==========================================
echo.

echo Instalando CustomTkinter...
pip install customtkinter>=5.2.0
echo.

echo Instalando Pandas...
pip install pandas>=1.5.0
echo.

echo Instalando PyET...
pip install pyet>=1.4.0
echo.

echo Instalando PyInstaller...
pip install pyinstaller>=5.0.0
echo.

echo ==========================================
echo  Instalacion completada!
echo  Ejecute: python calculadora_et0.py
echo ==========================================
echo.
pause 