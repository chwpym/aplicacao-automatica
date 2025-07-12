#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para o provedor Nakata
Testa o parser HTML e a extração de dados da tabela de aplicações
"""

import requests
from bs4 import BeautifulSoup, Tag
import json
import re

def test_nakata_parser():
    """Testa o parser Nakata com um ID real"""
    
    # ID de teste (pivô de suspensão N 3045)
    test_id = "n-3045-pivo-de-suspensao-1418"
    
    # URL do catálogo Nakata
    url = f"https://www.catalogonakata.com.br/detalhe/{test_id}"
    
    # Headers baseados na configuração atualizada
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A )Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "origin": "https://www.catalogonakata.com.br",
        "referer": f"https://www.catalogonakata.com.br/detalhe/{test_id}"
    }
    
    print(f"🔍 Testando provedor Nakata...")
    print(f"📡 URL: {url}")
    print(f"🆔 ID: {test_id}")
    print("-" * 50)
    
    try:
        # Faz a requisição
        print("📡 Fazendo requisição HTTP...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"📏 Tamanho: {len(response.content)} bytes")
        
        # Parse HTML
        print("\n🔍 Fazendo parsing HTML...")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Testa o parser Nakata
        print("\n🚗 Testando parser Nakata...")
        from app_catalogo import parse_nakata_html
        
        vehicles = parse_nakata_html(soup)
        
        print(f"✅ Veículos encontrados: {len(vehicles)}")
        
        if vehicles:
            print("\n📋 Resultados:")
            print("-" * 80)
            for i, vehicle in enumerate(vehicles, 1):
                print(f"\n🚗 Veículo {i}:")
                print(f"   Marca: {vehicle.get('brand', 'N/A')}")
                print(f"   Modelo: {vehicle.get('model', 'N/A')}")
                print(f"   Ano: {vehicle.get('startYear', 'N/A')} - {vehicle.get('endYear', 'N/A')}")
                print(f"   Posição: {vehicle.get('position', 'N/A')}")
                print(f"   Lado: {vehicle.get('side', 'N/A')}")
                print(f"   Direção: {vehicle.get('steering', 'N/A')}")
                print(f"   Observação: {vehicle.get('note', 'N/A')}")
                print(f"   Motor: {vehicle.get('engineName', 'N/A')}")
        else:
            print("❌ Nenhum veículo encontrado!")
            
            # Debug: mostra as tabelas encontradas
            tables = soup.find_all('table')
            print(f"\n🔍 Tabelas encontradas: {len(tables)}")
            for i, table in enumerate(tables):
                if isinstance(table, Tag):
                    headers = [th.get_text(strip=True) for th in table.find_all('th')]
                    print(f"   Tabela {i+1}: {headers}")
                else:
                    print(f"   Tabela {i+1}: [NÃO É TAG]")
        
        # Salva o HTML para debug se necessário
        with open("nakata_debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"\n💾 HTML salvo em: nakata_debug.html")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de requisição: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()

def test_nakata_integration():
    """Testa a integração completa com o sistema"""
    
    print("\n" + "="*60)
    print("🔧 TESTE DE INTEGRAÇÃO COMPLETA")
    print("="*60)
    
    try:
        from app_catalogo import buscar_provedor_generico, load_provedores
        
        # Carrega configuração dos provedores
        provedores = load_provedores()
        nakata_config = provedores.get('nakata')
        
        if not nakata_config:
            print("❌ Configuração do Nakata não encontrada!")
            return
        
        print(f"✅ Configuração carregada: {nakata_config['nome']}")
        
        # Testa com ID real
        test_id = "n-3045-pivo-de-suspensao-1418"
        
        print(f"\n🔍 Testando busca com ID: {test_id}")
        vehicles = buscar_provedor_generico(test_id, nakata_config)
        
        print(f"✅ Resultado: {len(vehicles)} veículos encontrados")
        
        if vehicles:
            print("\n📋 Primeiros 3 resultados:")
            for i, vehicle in enumerate(vehicles[:3], 1):
                print(f"\n🚗 {i}. {vehicle.get('brand', '')} {vehicle.get('model', '')}")
                print(f"   Ano: {vehicle.get('startYear', '')} - {vehicle.get('endYear', '')}")
                print(f"   Obs: {vehicle.get('note', '')}")
        
    except Exception as e:
        print(f"❌ Erro na integração: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 TESTE DO PROVEDOR NAKATA")
    print("="*50)
    
    # Teste básico do parser
    test_nakata_parser()
    
    # Teste de integração
    test_nakata_integration()
    
    print("\n✅ Teste concluído!") 