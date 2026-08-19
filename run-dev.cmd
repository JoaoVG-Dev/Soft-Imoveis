@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%" || exit /b 1

if defined SOFTIMOVEIS_PYTHON (
    set "PYTHON=%SOFTIMOVEIS_PYTHON%"
) else if exist "%ROOT%.venv\Scripts\python.exe" (
    set "PYTHON=%ROOT%.venv\Scripts\python.exe"
) else (
    for /f "delims=" %%P in ('where python.exe 2^>nul') do (
        set "PYTHON=%%P"
        goto :python_found
    )
)

:python_found
if not defined PYTHON (
    echo Python nao encontrado.
    echo.
    echo Crie o ambiente:
    echo python -m venv .venv
    echo .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    exit /b 1
)

echo Soft-Imoveis DEV RUN
"%PYTHON%" --version
if errorlevel 1 (
    echo Python configurado nao pode ser executado: %PYTHON%
    exit /b 1
)

if /I "%~1"=="-SmokeTest" (
    "%PYTHON%" -m src.main --smoke-test
) else (
    "%PYTHON%" -m src.main %*
)
exit /b %ERRORLEVEL%
