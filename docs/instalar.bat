@echo off
chcp 65001 >nul
title Instalador do Sistema de Catálogo Automotivo

echo.
echo ============================================================
echo 🚗 INSTALADOR DO SISTEMA DE CATÁLOGO AUTOMOTIVO
echo ============================================================
echo.

echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale o Python 3.7+ primeiro.
    echo    Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado!

echo.
echo 📦 Instalando dependências...
echo.

pip install requests pyperclip beautifulsoup4 ttkthemes

if errorlevel 1 (
    echo ❌ Erro ao instalar dependências!
    pause
    exit /b 1
)

echo.
echo ✅ Dependências instaladas!

echo.
echo 🖥️ Criando atalho na área de trabalho...

set "desktop=%USERPROFILE%\Desktop"
if not exist "%desktop%" set "desktop=%USERPROFILE%\Área de Trabalho"

if exist "%desktop%" (
    echo @echo off > "%desktop%\Catálogo Automotivo.bat"
    echo cd /d "%~dp0" >> "%desktop%\Catálogo Automotivo.bat"
    echo python app_catalogo_cursor.py >> "%desktop%\Catálogo Automotivo.bat"
    echo pause >> "%desktop%\Catálogo Automotivo.bat"
    echo ✅ Atalho criado: %desktop%\Catálogo Automotivo.bat
) else (
    echo ⚠️ Área de trabalho não encontrada
)

echo.
echo ============================================================
echo ✅ INSTALAÇÃO CONCLUÍDA!
echo ============================================================
echo.
echo 🎉 O Sistema de Catálogo Automotivo foi instalado!
echo.
echo 📋 Como usar:
echo    • Área de Trabalho: Clique no atalho 'Catálogo Automotivo'
echo    • Linha de Comando: python app_catalogo_cursor.py
echo.
echo ============================================================
pause 