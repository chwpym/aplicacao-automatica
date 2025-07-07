#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Diagnóstico do Sistema de Catálogo Automotivo
"""

import os
import sys
import json
import importlib
import traceback
from datetime import datetime

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def check_python():
    """Verifica versão do Python"""
    print_header("VERIFICAÇÃO DO PYTHON")
    
    print(f"Versão: {sys.version}")
    print(f"Executável: {sys.executable}")
    print(f"Plataforma: {sys.platform}")
    
    if sys.version_info >= (3, 7):
        print("✅ Python compatível")
        return True
    else:
        print("❌ Python muito antigo - precisa 3.7+")
        return False

def check_dependencies():
    """Verifica dependências"""
    print_header("VERIFICAÇÃO DE DEPENDÊNCIAS")
    
    dependencies = {
        'tkinter': 'Interface gráfica',
        'requests': 'Requisições HTTP',
        'pyperclip': 'Área de transferência',
        'bs4': 'BeautifulSoup - parsing HTML',
        'ttkthemes': 'Temas visuais',
        'json': 'Processamento JSON',
        'csv': 'Exportação CSV'
    }
    
    all_ok = True
    
    for module, description in dependencies.items():
        try:
            importlib.import_module(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description} - ERRO: {e}")
            all_ok = False
    
    return all_ok

def check_files():
    """Verifica arquivos essenciais"""
    print_header("VERIFICAÇÃO DE ARQUIVOS")
    
    essential_files = [
        ('app_catalogo_cursor.py', 'Aplicativo principal'),
        ('provedores.json', 'Configuração de provedores'),
        ('siglas.json', 'Siglas de marcas'),
        ('palavras_remover.json', 'Palavras para remover')
    ]
    
    all_ok = True
    
    for filename, description in essential_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} - {description} ({size} bytes)")
        else:
            print(f"❌ {filename} - {description} - ARQUIVO NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def check_json_files():
    """Verifica se arquivos JSON são válidos"""
    print_header("VERIFICAÇÃO DE ARQUIVOS JSON")
    
    json_files = ['provedores.json', 'siglas.json', 'palavras_remover.json']
    all_ok = True
    
    for filename in json_files:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {filename} - JSON válido")
            except json.JSONDecodeError as e:
                print(f"❌ {filename} - JSON inválido: {e}")
                all_ok = False
            except Exception as e:
                print(f"❌ {filename} - Erro ao ler: {e}")
                all_ok = False
        else:
            print(f"⚠️ {filename} - Arquivo não encontrado")
    
    return all_ok

def check_providers():
    """Verifica configuração de provedores"""
    print_header("VERIFICAÇÃO DE PROVEDORES")
    
    try:
        with open('provedores.json', 'r', encoding='utf-8') as f:
            providers = json.load(f)
        
        print(f"Total de provedores: {len(providers)}")
        
        for key, provider in providers.items():
            nome = provider.get('nome', 'N/A')
            tipo = provider.get('tipo', 'N/A')
            ativo = provider.get('ativo', False)
            url = provider.get('url', 'N/A')
            
            status = "✅ Ativo" if ativo else "❌ Inativo"
            print(f"   {nome} ({tipo}) - {status}")
            print(f"      URL: {url}")
            
            # Verificar campos obrigatórios
            required_fields = ['nome', 'tipo', 'url']
            missing_fields = [field for field in required_fields if field not in provider]
            
            if missing_fields:
                print(f"      ⚠️ Campos faltando: {', '.join(missing_fields)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar provedores: {e}")
        return False

def test_main_app():
    """Testa o aplicativo principal"""
    print_header("TESTE DO APLICATIVO PRINCIPAL")
    
    try:
        # Importa o módulo principal
        import app_catalogo_cursor
        
        print("✅ Módulo principal importado com sucesso")
        
        # Testa criação da janela (sem mostrar)
        try:
            root = app_catalogo_cursor.ThemedTk(theme="arc")
            app = app_catalogo_cursor.Application(root)
            root.destroy()
            print("✅ Interface criada com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar interface: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao importar aplicativo: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def check_permissions():
    """Verifica permissões de arquivo"""
    print_header("VERIFICAÇÃO DE PERMISSÕES")
    
    test_files = ['app_catalogo_cursor.py', 'provedores.json']
    all_ok = True
    
    for filename in test_files:
        if os.path.exists(filename):
            try:
                # Testa leitura
                with open(filename, 'r', encoding='utf-8') as f:
                    f.read(100)
                print(f"✅ {filename} - Leitura OK")
                
                # Testa escrita (cria arquivo temporário)
                test_file = f"test_write_{filename}"
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                print(f"✅ {filename} - Escrita OK")
                
            except PermissionError:
                print(f"❌ {filename} - Sem permissão de leitura/escrita")
                all_ok = False
            except Exception as e:
                print(f"❌ {filename} - Erro: {e}")
                all_ok = False
    
    return all_ok

def generate_report():
    """Gera relatório de diagnóstico"""
    print_header("RELATÓRIO DE DIAGNÓSTICO")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
RELATÓRIO DE DIAGNÓSTICO - {timestamp}
===============================================

Sistema: Sistema de Catálogo Automotivo
Versão: 1.0
Data: {timestamp}

VERIFICAÇÕES:
"""
    
    checks = [
        ("Python", check_python()),
        ("Dependências", check_dependencies()),
        ("Arquivos", check_files()),
        ("JSON", check_json_files()),
        ("Provedores", check_providers()),
        ("Aplicativo", test_main_app()),
        ("Permissões", check_permissions())
    ]
    
    all_passed = True
    
    for check_name, result in checks:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        report += f"{check_name}: {status}\n"
        if not result:
            all_passed = False
    
    report += f"""
RESULTADO FINAL: {'✅ SISTEMA OK' if all_passed else '❌ PROBLEMAS ENCONTRADOS'}

RECOMENDAÇÕES:
"""
    
    if all_passed:
        report += "- Sistema funcionando corretamente\n"
        report += "- Pode usar normalmente\n"
    else:
        report += "- Verificar problemas identificados acima\n"
        report += "- Executar instalar.bat para reinstalar dependências\n"
        report += "- Verificar permissões de arquivo\n"
    
    # Salva relatório
    report_file = f"diagnostico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"📄 Relatório salvo: {report_file}")
    
    return all_passed

def main():
    """Função principal"""
    print("🚗 DIAGNÓSTICO DO SISTEMA DE CATÁLOGO AUTOMOTIVO")
    print("="*60)
    
    success = generate_report()
    
    print("\n" + "="*60)
    if success:
        print("✅ DIAGNÓSTICO CONCLUÍDO - SISTEMA OK")
    else:
        print("❌ DIAGNÓSTICO CONCLUÍDO - PROBLEMAS ENCONTRADOS")
        print("\n🔧 SOLUÇÕES:")
        print("1. Execute: .\\instalar.bat")
        print("2. Execute: .\\atualizar.bat")
        print("3. Verifique permissões de arquivo")
    print("="*60)

if __name__ == "__main__":
    main() 