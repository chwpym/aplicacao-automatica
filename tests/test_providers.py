#!/usr/bin/env python3
"""
Teste completo dos provedores de dados
Testa Authomix, Sabo e Nakata
"""

import json
import requests
from bs4 import BeautifulSoup
import re

def test_authomix_provider():
    """Testa o provedor Authomix"""
    print("=" * 50)
    print("Testando Provedor Authomix")
    print("=" * 50)
    
    # Configuração do Authomix
    authomix_config = {
        "nome": "Authomix",
        "url": "https://bff.catalogofraga.com.br/gateway/graphql",
        "ativo": True,
        "tipo": "graphql",
        "headers": {
            "origin": "https://catalogo.authomix.com.br",
            "referer": "https://catalogo.authomix.com.br/"
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
    
    # ID de teste (você pode alterar para um ID válido)
    test_id = "5042ecad-dbcb-92314cc6-2fb6-6b213869-a827"
    
    try:
        from app_catalogo_cursor import buscar_provedor_generico
        vehicles = buscar_provedor_generico(test_id, authomix_config)
        
        if vehicles:
            print(f"✅ Authomix: {len(vehicles)} veículos encontrados")
            for i, vehicle in enumerate(vehicles[:3]):  # Mostra apenas os 3 primeiros
                print(f"  Veículo {i+1}: {vehicle.get('brand', '')} {vehicle.get('name', '')} {vehicle.get('engineName', '')}")
        else:
            print("⚠️ Authomix: Nenhum veículo encontrado (pode ser um ID inválido)")
            
    except Exception as e:
        print(f"❌ Erro no Authomix: {e}")

def test_sabo_provider():
    """Testa o provedor Sabo"""
    print("\n" + "=" * 50)
    print("Testando Provedor Sabo")
    print("=" * 50)
    
    # Configuração do Sabo
    sabo_config = {
        "nome": "Sabo",
        "url": "https://bff.catalogofraga.com.br/gateway/graphql",
        "ativo": True,
        "tipo": "graphql",
        "headers": {
            "origin": "https://catalogo.sabo.com.br",
            "referer": "https://catalogo.sabo.com.br/"
        },
        "query": """query GetProductById($id: String!, $market: MarketType!) {
  product(id: $id, market: $market) {
    vehicles {
      engineConfiguration
      transmissionManufacturer
      brand
      model
      engineName
      name
      transmissionType
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
    
    # ID de teste (você pode alterar para um ID válido)
    test_id = "5042ecad-dbcb-92314cc6-2fb6-6b213869-a827"
    
    try:
        from app_catalogo_cursor import buscar_provedor_generico
        vehicles = buscar_provedor_generico(test_id, sabo_config)
        
        if vehicles:
            print(f"✅ Sabo: {len(vehicles)} veículos encontrados")
            for i, vehicle in enumerate(vehicles[:3]):  # Mostra apenas os 3 primeiros
                print(f"  Veículo {i+1}: {vehicle.get('brand', '')} {vehicle.get('name', '')} {vehicle.get('engineName', '')}")
        else:
            print("⚠️ Sabo: Nenhum veículo encontrado (pode ser um ID inválido)")
            
    except Exception as e:
        print(f"❌ Erro no Sabo: {e}")

def test_nakata_provider():
    """Testa o provedor Nakata"""
    print("\n" + "=" * 50)
    print("Testando Provedor Nakata")
    print("=" * 50)
    
    # Configuração do Nakata
    nakata_config = {
        "nome": "Catálogo Nakata",
        "url": "https://www.nakata.com.br/catalogo/aplicacao/{id}",
        "ativo": True,
        "tipo": "rest",
        "headers": {
            "origin": "https://www.nakata.com.br",
            "referer": "https://www.nakata.com.br/"
        },
        "query": ""
    }
    
    # ID de teste
    test_id = "exemplo-123"
    
    try:
        from app_catalogo_cursor import buscar_provedor_generico
        vehicles = buscar_provedor_generico(test_id, nakata_config)
        
        if vehicles:
            print(f"✅ Nakata: {len(vehicles)} veículos encontrados")
            for i, vehicle in enumerate(vehicles):
                print(f"  Veículo {i+1}: {vehicle.get('brand', '')} {vehicle.get('name', '')} {vehicle.get('engineName', '')} {vehicle.get('startYear', '')}-{vehicle.get('endYear', '')}")
        else:
            print("⚠️ Nakata: Nenhum veículo encontrado")
            
    except Exception as e:
        print(f"❌ Erro no Nakata: {e}")

def test_provider_manager():
    """Testa o sistema de gerenciamento de provedores"""
    print("\n" + "=" * 50)
    print("Testando Sistema de Provedores")
    print("=" * 50)
    
    try:
        from app_catalogo_cursor import load_provedores, save_provedores
        
        # Carrega provedores existentes
        provedores = load_provedores()
        print(f"✅ Provedores carregados: {len(provedores)} encontrados")
        
        # Lista os provedores
        for key, provedor in provedores.items():
            status = "✅ Ativo" if provedor.get('ativo', False) else "❌ Inativo"
            print(f"  - {provedor.get('nome', '')} ({provedor.get('tipo', '')}) - {status}")
        
        # Testa salvamento
        save_provedores(provedores)
        print("✅ Provedores salvos com sucesso")
        
    except Exception as e:
        print(f"❌ Erro no sistema de provedores: {e}")

def main():
    """Função principal de teste"""
    print("🚀 TESTE COMPLETO DOS PROVEDORES DE DADOS")
    print("=" * 60)
    
    # Testa cada provedor
    test_authomix_provider()
    test_sabo_provider()
    test_nakata_provider()
    test_provider_manager()
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 60)
    print("\nPara testar com IDs reais:")
    print("1. Execute: python app_catalogo_cursor.py")
    print("2. Digite um ID válido de peça")
    print("3. Selecione o provedor desejado")
    print("4. Clique em 'Buscar Aplicações'")

if __name__ == "__main__":
    main() 