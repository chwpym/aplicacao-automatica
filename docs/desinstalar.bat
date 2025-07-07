@echo off
chcp 65001 >nul
title Desinstalador do Sistema de Catálogo Automotivo

echo.
echo ============================================================
echo 🗑️ DESINSTALADOR DO SISTEMA DE CATÁLOGO AUTOMOTIVO
echo ============================================================
echo.

echo 🖥️ Removendo atalho da área de trabalho...

set "desktop=%USERPROFILE%\Desktop"
if not exist "%desktop%" set "desktop=%USERPROFILE%\Área de Trabalho"

if exist "%desktop%\Catálogo Automotivo.bat" (
    del "%desktop%\Catálogo Automotivo.bat"
    echo ✅ Atalho removido da área de trabalho
) else (
    echo ⚠️ Atalho não encontrado na área de trabalho
)

echo.
echo 📦 Removendo dependências...

pip uninstall -y requests pyperclip beautifulsoup4 ttkthemes

echo.
echo ============================================================
echo ✅ DESINSTALAÇÃO CONCLUÍDA!
echo ============================================================
echo.
echo 🗑️ O Sistema de Catálogo Automotivo foi removido!
echo.
echo 📝 Nota: Os arquivos do sistema ainda estão na pasta atual.
echo    Para remover completamente, delete a pasta do projeto.
echo.
echo ============================================================
pause 