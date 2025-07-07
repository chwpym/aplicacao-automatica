#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de desinstalação do Sistema de Catálogo
"""

import os
import sys
import subprocess
from pathlib import Path

def remove_shortcuts():
    """Remove atalhos criados"""
    try:
        # Remove atalho da área de trabalho
        desktop = Path.home() / "Desktop"
        if not desktop.exists():
            desktop = Path.home() / "Área de Trabalho"
        
        bat_file = desktop / "Catálogo Automotivo.bat"
        if bat_file.exists():
            bat_file.unlink()
            print("✅ Atalho da área de trabalho removido")
        
        # Remove pasta do menu iniciar
        start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Catálogo Automotivo"
        if start_menu.exists():
            shutil.rmtree(start_menu)
            print("✅ Atalho do menu iniciar removido")
            
    except Exception as e:
        print(f"⚠️ Erro ao remover atalhos: {e}")

def uninstall_packages():
    """Remove pacotes instalados"""
    packages = ["requests", "pyperclip", "beautifulsoup4", "ttkthemes"]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])
            print(f"✅ {package} removido")
        except:
            print(f"⚠️ {package} não encontrado")

if __name__ == "__main__":
    print("🗑️ Desinstalando Sistema de Catálogo...")
    remove_shortcuts()
    uninstall_packages()
    print("✅ Desinstalação concluída!")
    input("Pressione Enter para sair...")
