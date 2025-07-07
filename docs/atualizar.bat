@echo off
chcp 65001 >nul
title Atualizador do Sistema de Catálogo Automotivo

echo.
echo ============================================================
echo 🔄 ATUALIZADOR DO SISTEMA DE CATÁLOGO AUTOMOTIVO
echo ============================================================
echo.

echo 📅 Criando backup...
set "timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "timestamp=%timestamp: =0%"
set "backup_dir=backup_%timestamp%"

if not exist "%backup_dir%" mkdir "%backup_dir%"

echo    Fazendo backup dos arquivos principais...
copy "app_catalogo_cursor.py" "%backup_dir%\" >nul
copy "provedores.json" "%backup_dir%\" >nul
copy "siglas.json" "%backup_dir%\" >nul
copy "palavras_remover.json" "%backup_dir%\" >nul

echo    ✅ Backup criado: %backup_dir%

echo.
echo 🔄 Verificando atualizações...

echo    Verificando dependências...
pip install --upgrade requests pyperclip beautifulsoup4 ttkthemes

echo.
echo ✅ Sistema atualizado!

echo.
echo 📋 Próximos passos:
echo    1. Teste o sistema: python app_catalogo_cursor.py
echo    2. Se houver problemas, restaure o backup: %backup_dir%
echo    3. Para restaurar: copy "%backup_dir%\*.*" "."
echo.

echo ============================================================
pause 