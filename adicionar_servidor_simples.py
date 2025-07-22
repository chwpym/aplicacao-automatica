#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para adicionar um novo servidor/provedor ao sistema de catálogos.
Versão sem dependência do tkinter.
"""

import json
import os

def load_provedores(filename="provedores.json"):
    """Carrega provedores do arquivo JSON"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Arquivo '{filename}' corrompido. Criando novo.")
            return {}
    return {}

def save_provedores(provedores_data, filename="provedores.json"):
    """Salva provedores no arquivo JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(provedores_data, f, indent=4, ensure_ascii=False)

def adicionar_novo_servidor():
    """Adiciona um novo servidor ao arquivo provedores.json"""
    
    print("=== ADICIONAR NOVO SERVIDOR ===")
    print()
    
    # Carrega os provedores existentes
    provedores = load_provedores()
    
    # Coleta informações do usuário
    print("1. Informações básicas:")
    nome = input("Nome do provedor: ").strip()
    if not nome:
        print("❌ Nome é obrigatório!")
        return
    
    url = input("URL da API: ").strip()
    if not url:
        print("❌ URL é obrigatória!")
        return
    
    print("\n2. Tipo de API:")
    print("   1 - GraphQL")
    print("   2 - REST")
    print("   3 - Local")
    print("   4 - Custom (viemar, iguacu, etc.)")
    
    tipo_opcao = input("Escolha (1-4): ").strip()
    tipo_map = {
        "1": "graphql",
        "2": "rest", 
        "3": "local",
        "4": "custom"
    }
    
    tipo = tipo_map.get(tipo_opcao, "rest")
    
    # Se for custom, pede o tipo específico
    if tipo == "custom":
        tipo = input("Tipo específico (ex: viemar, iguacu, mte_thomson): ").strip()
    
    print(f"\n3. Headers (para provedores web):")
    origin = input("Origin (opcional): ").strip()
    referer = input("Referer (opcional): ").strip()
    
    # Configuração específica por tipo
    config = {
        "nome": nome,
        "url": url,
        "tipo": tipo,
        "ativo": True,
        "headers": {}
    }
    
    # Adiciona headers se fornecidos
    if origin:
        config["headers"]["origin"] = origin
    if referer:
        config["headers"]["referer"] = referer
    
    # Headers específicos para REST
    if tipo == "rest":
        config["headers"].update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd"
        })
        config["query"] = ""
    
    # Query padrão para GraphQL
    elif tipo == "graphql":
        config["query"] = """query GetProductById($id: String!, $market: MarketType!) {
  product(id: $id, market: $market) {
    vehicles {
      brand
      name
      model
      engineName
      engineConfiguration
      endYear
      note
      only
      restriction
      startYear
      __typename
    }
  }
}"""
    
    # Para tipos especiais, apenas adiciona configuração básica
    else:
        config["query"] = ""
    
    # Gera chave única
    chave = nome.lower().replace(' ', '_').replace('-', '_')
    
    # Verifica se já existe
    if chave in provedores:
        resposta = input(f"\n⚠️ Provedor '{nome}' já existe. Substituir? (s/N): ").strip().lower()
        if resposta != 's':
            print("❌ Operação cancelada.")
            return
    
    # Adiciona o novo provedor
    provedores[chave] = config
    
    # Salva o arquivo
    try:
        save_provedores(provedores)
        print(f"\n✅ Servidor '{nome}' adicionado com sucesso!")
        print(f"   Chave: {chave}")
        print(f"   Tipo: {tipo}")
        print(f"   URL: {url}")
        print(f"   Ativo: {config['ativo']}")
        
        # Mostra um exemplo de como testar
        print(f"\n💡 Para testar, use a aplicação principal e selecione o provedor '{nome}'")
        
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")

def listar_servidores():
    """Lista os servidores existentes"""
    print("=== SERVIDORES EXISTENTES ===")
    print()
    
    provedores = load_provedores()
    
    if not provedores:
        print("❌ Nenhum servidor encontrado.")
        return
    
    for chave, config in provedores.items():
        status = "✅ ATIVO" if config.get('ativo', False) else "❌ INATIVO"
        print(f"🔹 {config.get('nome', chave)}")
        print(f"   Chave: {chave}")
        print(f"   Tipo: {config.get('tipo', 'N/A')}")
        print(f"   URL: {config.get('url', 'N/A')}")
        print(f"   Status: {status}")
        print()

def adicionar_exemplo_rapido():
    """Adiciona um servidor de exemplo para demonstração"""
    print("=== ADICIONANDO SERVIDOR DE EXEMPLO ===")
    print()
    
    provedores = load_provedores()
    
    # Exemplo de servidor GraphQL
    exemplo_config = {
        "nome": "Exemplo GraphQL",
        "url": "https://api.exemplo.com/graphql",
        "tipo": "graphql",
        "ativo": True,
        "headers": {
            "origin": "https://catalogo.exemplo.com",
            "referer": "https://catalogo.exemplo.com/"
        },
        "query": """query GetProductById($id: String!, $market: MarketType!) {
  product(id: $id, market: $market) {
    vehicles {
      brand
      name
      model
      engineName
      engineConfiguration
      endYear
      note
      only
      restriction
      startYear
      __typename
    }
  }
}"""
    }
    
    chave = "exemplo_graphql"
    provedores[chave] = exemplo_config
    
    try:
        save_provedores(provedores)
        print("✅ Servidor de exemplo adicionado com sucesso!")
        print(f"   Nome: {exemplo_config['nome']}")
        print(f"   Chave: {chave}")
        print(f"   Tipo: {exemplo_config['tipo']}")
        print(f"   URL: {exemplo_config['url']}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")

def menu_principal():
    """Menu principal do script"""
    while True:
        print("=== GERENCIADOR DE SERVIDORES ===")
        print()
        print("1. Adicionar novo servidor")
        print("2. Listar servidores existentes")
        print("3. Adicionar servidor de exemplo")
        print("4. Sair")
        print()
        
        opcao = input("Escolha uma opção (1-4): ").strip()
        print()
        
        if opcao == "1":
            adicionar_novo_servidor()
        elif opcao == "2":
            listar_servidores()
        elif opcao == "3":
            adicionar_exemplo_rapido()
        elif opcao == "4":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    menu_principal()