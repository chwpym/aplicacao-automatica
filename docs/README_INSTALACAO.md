# Sistema de Catálogo Automotivo

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
