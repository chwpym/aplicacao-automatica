#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a formatação dos campos selecionados
"""

def test_formato_campos():
    """Testa a formatação dos campos selecionados"""
    
    # Simula dados do Nakata
    test_vehicles = [
        {
            'brand': 'GENERAL MOTORS',
            'model': 'Celta',
            'engineName': '',
            'startYear': 2000,
            'endYear': 2010,
            'note': 'Posição: Dianteiro Inferior / Inferior; Lado: Direito / Esquerdo; Direção: Hidráulica / Mecânica',
            'position': 'Dianteiro Inferior / Inferior',
            'side': 'Direito / Esquerdo',
            'steering': 'Hidráulica / Mecânica'
        },
        {
            'brand': 'GENERAL MOTORS',
            'model': 'Corsa',
            'engineName': '',
            'startYear': 1998,
            'endYear': 2002,
            'note': 'Posição: Dianteiro Inferior / Inferior; Lado: Direito / Esquerdo; Direção: Hidráulica / Mecânica',
            'position': 'Dianteiro Inferior / Inferior',
            'side': 'Direito / Esquerdo',
            'steering': 'Hidráulica / Mecânica'
        }
    ]
    
    # Simula campos selecionados
    field_vars = {
        'marca': True,
        'modelo': True,
        'motor': False,  # Não selecionado
        'ano': True,
        'observacao': False,  # Não selecionado
        'posicao': True,
        'lado': False,  # Não selecionado
        'direcao': True
    }
    
    available_fields = {
        'marca': 'Marca',
        'modelo': 'Modelo',
        'motor': 'Motor',
        'configuracao_motor': 'Configuração Motor',
        'ano': 'Ano',
        'observacao': 'Observação',
        'sistema_freio': 'Sistema de Freio',
        'restricao': 'Restrição',
        'apenas': 'Apenas',
        'posicao': 'Posição',
        'lado': 'Lado',
        'direcao': 'Direção'
    }
    
    print("🧪 TESTE DE FORMATAÇÃO DOS CAMPOS")
    print("="*50)
    
    # Processa os dados
    applications_for_clipboard = []
    
    for vehicle in test_vehicles:
        # Mapeia os dados
        full_field_values = {
            'marca': vehicle.get('brand', ''),
            'modelo': vehicle.get('model', ''),
            'motor': vehicle.get('engineName', ''),
            'configuracao_motor': '',
            'ano': f"{vehicle.get('startYear', '')}...{vehicle.get('endYear', '')}",
            'observacao': vehicle.get('note', ''),
            'sistema_freio': '',
            'restricao': '',
            'apenas': '',
            'posicao': vehicle.get('position', ''),
            'lado': vehicle.get('side', ''),
            'direcao': vehicle.get('steering', '')
        }
        
        # Filtra apenas campos selecionados
        output_parts_clipboard = []
        for field_key in field_vars.keys():
            if field_vars[field_key]:  # Só inclui se o campo estiver selecionado
                value = full_field_values.get(field_key)
                if value:
                    output_parts_clipboard.append(str(value))
        
        aplicacao_formatada_clipboard = " ".join(output_parts_clipboard).strip()
        if aplicacao_formatada_clipboard:
            applications_for_clipboard.append(aplicacao_formatada_clipboard)
    
    # Mostra resultados
    print(f"✅ Aplicações formatadas: {len(applications_for_clipboard)}")
    print("\n📋 Campos selecionados:")
    for field, selected in field_vars.items():
        status = "✅" if selected else "❌"
        print(f"   {status} {available_fields[field]}")
    
    print("\n📄 Resultado formatado:")
    print("-" * 50)
    for i, app in enumerate(applications_for_clipboard, 1):
        print(f"{i}. {app}")
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    test_formato_campos() 