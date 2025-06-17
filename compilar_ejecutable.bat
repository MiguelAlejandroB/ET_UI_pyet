@echo off
echo ==========================================
echo  Compilador de Calculadora ET0
echo  Generando ejecutable con PyInstaller...
echo ==========================================
echo.

if not exist calculadora_et0.py (
    echo Error: No se encuentra el archivo calculadora_et0.py
    pause
    exit /b 1
)

echo Compilando aplicacion...
pyinstaller --onefile --windowed --name "CalculadoraET0" --distpath "./ejecutable" calculadora_et0.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo  Compilacion exitosa!
    echo  Ejecutable generado en: ./ejecutable/
    echo ==========================================
    echo.
    if exist "./ejecutable/CalculadoraET0.exe" (
        echo Archivo: CalculadoraET0.exe
        echo Tamaño: 
        dir "./ejecutable/CalculadoraET0.exe" | find "CalculadoraET0.exe"
    )
) else (
    echo.
    echo ==========================================
    echo  Error en la compilacion!
    echo  Verifique las dependencias.
    echo ==========================================
)

echo.
pause 