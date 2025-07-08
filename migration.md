# Plano de Migração do Projeto

Este documento serve para acompanhar, passo a passo, a migração e refatoração do sistema para uma estrutura modular, segura e sustentável.

## Checklist de Migração

- [ ] **1. Modularização dos Provedores**
    - [x] Migrar parsers REST para `providers/rest_parsers.py`
    - [x] Migrar lógica de busca dos provedores REST para `providers/rest.py`
    - [ ] Migrar provedores de outros tipos (PDF, GraphQL, etc.) para seus módulos

- [x] **2. Modularização dos Utilitários**
    - [x] Migrar funções auxiliares (backup, limpeza, configs) para `utils/`
    - [x] Ajustar imports para usar utilitários

- [ ] **3. Modularização da Interface**
    - [ ] Separar widgets/componentes auxiliares em `interface/`
    - [ ] Separar janela principal em `interface/main_window.py`

- [ ] **4. Refatoração para Orientação a Objetos**
    - [ ] Implementar classes base (ex: `BaseProvider`)
    - [ ] Refatorar provedores para herdar das bases
    - [ ] Refatorar interface para usar classes/componentes

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

- [x] Parsers REST migrados para `providers/rest_parsers.py`
- [x] Lógica de busca dos provedores REST migrada para `providers/rest.py` (sistema testado e funcionando)
- [x] Funções utilitárias migradas para `utils/` e imports ajustados (sistema testado e funcionando)
- [ ] (Preencha aqui cada etapa concluída com data e observações) 