#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador do Sistema de Catálogo de Peças Automotivas
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

def print_banner():
    """Exibe o banner do instalador"""
    print("="*60)
    print("🚗 INSTALADOR DO SISTEMA DE CATÁLOGO AUTOMOTIVO")
    print("="*60)
    print("Sistema de busca de aplicações de peças automotivas")
    print("Suporte: Authomix, Sabo, Nakata e outros provedores")
    print("="*60)

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print("🔍 Verificando versão do Python...")
    
    if sys.version_info < (3, 7):
        print("❌ ERRO: Python 3.7 ou superior é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_requirements():
    """Instala as dependências necessárias"""
    print("\n📦 Instalando dependências...")
    
    requirements = [
        "requests>=2.25.0",
        "pyperclip>=1.8.0",
        "beautifulsoup4>=4.9.0",
        "ttkthemes>=3.2.0"
    ]
    
    for req in requirements:
        try:
            print(f"   Instalando {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"   ✅ {req} - OK")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro ao instalar {req}: {e}")
            return False
    
    return True

def create_desktop_shortcut():
    """Cria atalho na área de trabalho"""
    print("\n🖥️ Criando atalho na área de trabalho...")
    
    try:
        desktop = Path.home() / "Desktop"
        if not desktop.exists():
            desktop = Path.home() / "Área de Trabalho"
        
        if desktop.exists():
            # Cria arquivo .bat para Windows
            bat_content = f'''@echo off
cd /d "{os.getcwd()}"
python app_catalogo_cursor.py
pause
'''
            
            bat_file = desktop / "Catálogo Automotivo.bat"
            with open(bat_file, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            
            print(f"   ✅ Atalho criado: {bat_file}")
            return True
        else:
            print("   ⚠️ Área de trabalho não encontrada")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao criar atalho: {e}")
        return False

def create_start_menu_shortcut():
    """Cria atalho no menu iniciar"""
    print("\n📋 Criando atalho no menu iniciar...")
    
    try:
        start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
        if start_menu.exists():
            # Cria pasta para o aplicativo
            app_folder = start_menu / "Catálogo Automotivo"
            app_folder.mkdir(exist_ok=True)
            
            # Cria arquivo .bat
            bat_content = f'''@echo off
cd /d "{os.getcwd()}"
python app_catalogo_cursor.py
'''
            
            bat_file = app_folder / "Catálogo Automotivo.bat"
            with open(bat_file, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            
            print(f"   ✅ Atalho no menu iniciar criado")
            return True
        else:
            print("   ⚠️ Menu iniciar não encontrado")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao criar atalho no menu: {e}")
        return False

def verify_files():
    """Verifica se todos os arquivos necessários existem"""
    print("\n📁 Verificando arquivos do sistema...")
    
    required_files = [
        "app_catalogo_cursor.py",
        "provedores.json",
        "siglas.json",
        "palavras_remover.json"
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file} - OK")
        else:
            print(f"   ❌ {file} - FALTANDO")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Arquivos faltando: {', '.join(missing_files)}")
        return False
    
    return True

def create_uninstaller():
    """Cria script de desinstalação"""
    print("\n🗑️ Criando script de desinstalação...")
    
    uninstall_content = '''#!/usr/bin/env python3
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
'''
    
    with open("uninstall.py", 'w', encoding='utf-8') as f:
        f.write(uninstall_content)
    
    print("   ✅ Script de desinstalação criado: uninstall.py")

def create_readme():
    """Cria arquivo README com instruções"""
    print("\n📖 Criando documentação...")
    
    readme_content = '''# Sistema de Catálogo Automotivo

## Descrição
Sistema completo para busca de aplicações de peças automotivas com suporte a múltiplos provedores.

## Provedores Suportados
- **Authomix**: Busca via GraphQL
- **Sabo**: Busca via GraphQL  
- **Nakata**: Busca via REST/HTML

## Como Usar

### Iniciar o Sistema
1. **Atalho da Área de Trabalho**: Clique duas vezes no atalho "Catálogo Automotivo"
2. **Menu Iniciar**: Iniciar → Programas → Catálogo Automotivo
3. **Linha de Comando**: `python app_catalogo_cursor.py`

### Funcionalidades
- 🔍 Busca por ID de peça
- 📋 Seleção de campos para exibição
- 📤 Exportação para CSV
- 📋 Cópia para área de transferência
- 🎨 Temas visuais
- ⚙️ Configuração de provedores

### Campos Disponíveis
- Marca
- Modelo  
- Ano
- Motor
- Configuração Motor
- Posição
- Lado
- Direção
- Observações

## Configuração

### Provedores
Edite `provedores.json` para configurar provedores:
```json
{
  "nome": "Nome do Provedor",
  "tipo": "graphql|rest",
  "ativo": true,
  "url": "URL da API",
  "headers": {...}
}
```

### Siglas
Edite `siglas.json` para configurar siglas de marcas.

### Palavras para Remover
Edite `palavras_remover.json` para configurar palavras que devem ser removidas dos resultados.

## Desinstalação
Execute `python uninstall.py` para remover o sistema.

## Suporte
Para suporte técnico, consulte a documentação ou entre em contato com o desenvolvedor.

---
**Versão**: 1.0
**Data**: 2024
'''
    
    with open("README_INSTALACAO.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("   ✅ Documentação criada: README_INSTALACAO.md")

def main():
    """Função principal do instalador"""
    print_banner()
    
    # Verifica versão do Python
    if not check_python_version():
        input("\nPressione Enter para sair...")
        return
    
    # Verifica arquivos
    if not verify_files():
        print("\n❌ Instalação cancelada: arquivos necessários não encontrados")
        input("Pressione Enter para sair...")
        return
    
    # Instala dependências
    if not install_requirements():
        print("\n❌ Instalação cancelada: erro ao instalar dependências")
        input("Pressione Enter para sair...")
        return
    
    # Cria atalhos
    create_desktop_shortcut()
    create_start_menu_shortcut()
    
    # Cria scripts auxiliares
    create_uninstaller()
    create_readme()
    
    print("\n" + "="*60)
    print("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print("\n🎉 O Sistema de Catálogo Automotivo foi instalado!")
    print("\n📋 Como usar:")
    print("   • Área de Trabalho: Clique no atalho 'Catálogo Automotivo'")
    print("   • Menu Iniciar: Iniciar → Programas → Catálogo Automotivo")
    print("   • Linha de Comando: python app_catalogo_cursor.py")
    print("\n📖 Documentação: README_INSTALACAO.md")
    print("🗑️ Desinstalar: python uninstall.py")
    
    print("\n" + "="*60)
    input("Pressione Enter para finalizar...")

if __name__ == "__main__":
    main() 