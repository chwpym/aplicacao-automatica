# Plano de Migração do Projeto

Este documento serve para acompanhar, passo a passo, a migração e refatoração do sistema para uma estrutura modular, segura e sustentável.

## Checklist de Migração

- [x] **0. Estrutura de Pastas e Arquivos**
    - [x] Criar pastas `providers/`, `interface/`, `utils/` com `__init__.py`
    - [x] Criar arquivos-base: `base.py`, `rest.py`, `rest_parsers.py`, `main_window.py`, `layout_system.py`, `config.py`, `limpeza.py`, `backup.py`
    - [x] Adicionar docstrings explicativas nos esqueletos
- [x] **1. Modularização dos Provedores**
    - [x] Migrar parsers REST para `providers/rest_parsers.py`
    - [x] Migrar lógica de busca dos provedores REST para `providers/rest.py`
    - [x] Migrar provedor PDF para `providers/pdf.py` (classe PDFProvider)
    - [x] Migrar provedor GraphQL/Authomix para `providers/graphql.py` (classe AuthomixGraphQLProvider)
    - [x] Adaptar sistema principal para usar provedores modulares
    - [x] **Generalizar provider GraphQL:** Criado `GenericGraphQLProvider` em `providers/generic_graphql.py`, integração dinâmica com cadastro/interface/JSON, retrocompatibilidade garantida.

- [x] **2. Modularização dos Utilitários**
    - [x] Migrar funções auxiliares (backup, limpeza, configs) para `utils/`
    - [x] Ajustar imports para usar utilitários

- [x] **3. Modularização da Interface**
    - [x] Separar widgets/componentes auxiliares em `interface/` (ex: SearchBar, ResultsTable)
    - [x] Separar janela principal em `interface/main_window.py`
    - [x] Integrar interface modular à busca real: seleção dinâmica de provedor, busca conectada ao backend, exibição de resultados reais.

- [ ] **4. Refatoração para Orientação a Objetos**
    - [x] Implementar classes base (ex: `BaseProvider`)
    - [x] Refatorar provedores para herdar das bases (PDF, REST, GraphQL)
    - [x] Refatorar interface para usar classes/componentes

- [ ] **5. Limpeza e Remoção de Código Antigo**
    - [ ] Remover código antigo do arquivo principal após validação

- [ ] **6. Testes e Documentação**
    - [ ] Escrever testes para funções migradas
    - [ ] Atualizar README e comentários

---

## Dicas para Migração Segura
- Migre e teste em pequenas etapas.
- Nunca apague código funcional antes de garantir o novo.
- Faça commits frequentes e claros.
- Sempre rode o sistema após cada migração.
- Mantenha backup e use o GitHub como "ponto de restauração".
- Se possível, escreva testes automatizados para funções críticas.

---

## Histórico de Progresso

- [x] Estrutura de pastas e arquivos-base criada e documentada com docstrings (sistema pronto para modularização detalhada)
- [x] Parsers REST migrados para `providers/rest_parsers.py`
- [x] Lógica de busca dos provedores REST migrada para `providers/rest.py` (sistema testado e funcionando)
- [x] Funções utilitárias migradas para `utils/` e imports ajustados (sistema testado e funcionando)
- [x] Provedor PDF migrado para `providers/pdf.py` (classe PDFProvider) e sistema principal adaptado
- [x] Provedor GraphQL/Authomix migrado para `providers/graphql.py` (classe AuthomixGraphQLProvider) e sistema principal adaptado
- [x] **[2024-07-08] Generalização dos provedores GraphQL:** Criado `GenericGraphQLProvider` em `providers/generic_graphql.py`, integração dinâmica com cadastro/interface/JSON, todos os provedores GraphQL funcionando sem duplicação de código, retrocompatibilidade garantida.
- [x] **[2024-07-08] Modularização da interface concluída:**
    - Componentes SearchBar e ResultsTable criados e integrados.
    - Seleção dinâmica de provedor implementada.
    - Busca real conectada ao backend modularizado.
    - Interface pronta para evoluir com novas funções.

---

## Próxima Etapa

- Modularizar a interface:
    - Separar widgets/componentes auxiliares em `interface/`
    - Separar janela principal em `interface/main_window.py`
    - Refatorar interface para usar classes/componentes (orientação a objetos) 

---

## Melhorias Futuras Sugeridas
- Implementar busca em múltiplos provedores simultaneamente (feature sugerida e aprovada para pós-migração). 