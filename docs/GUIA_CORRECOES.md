# 🔧 Guia de Correções e Atualizações do Sistema

## 🚨 Como Identificar Problemas

### 1. **Logs de Erro**
```python
# Adicione logs para debug
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def funcao_problema():
    try:
        # código da função
        logger.info("Função executada com sucesso")
    except Exception as e:
        logger.error(f"Erro na função: {e}")
        # Tratamento do erro
```

### 2. **Testes Específicos**
```python
# Crie testes para funções específicas
def test_funcao_problema():
    # Teste com dados conhecidos
    resultado = funcao_problema(dados_teste)
    assert resultado == resultado_esperado
```

### 3. **Verificação de Dependências**
```bash
# Verifique se todas as dependências estão instaladas
pip list | grep -E "(requests|pyperclip|beautifulsoup4|ttkthemes)"
```

## 🛠️ Processo de Correção

### Passo 1: **Identificar o Problema**
- [ ] Qual função específica não funciona?
- [ ] Qual erro aparece?
- [ ] Quando o problema ocorre?
- [ ] Quais dados estão sendo usados?

### Passo 2: **Isolar o Problema**
- [ ] Criar teste mínimo reproduzível
- [ ] Verificar se é problema de dados ou código
- [ ] Testar em ambiente limpo

### Passo 3: **Corrigir o Código**
- [ ] Implementar a correção
- [ ] Adicionar tratamento de erros
- [ ] Testar a correção

### Passo 4: **Validar a Correção**
- [ ] Testar com dados reais
- [ ] Verificar se não quebrou outras funções
- [ ] Documentar a correção

## 📝 Como Atualizar o Sistema

### 1. **Backup Antes de Atualizar**
```bash
# Crie backup antes de qualquer mudança
cp app_catalogo_cursor.py app_catalogo_cursor_backup.py
cp provedores.json provedores_backup.json
```

### 2. **Atualizar Arquivos**
- [ ] Modificar o código principal
- [ ] Atualizar configurações se necessário
- [ ] Testar as mudanças

### 3. **Atualizar Instalador**
```python
# Se adicionar novas dependências, atualizar:
# - requirements.txt
# - installer.py
# - instalar.bat
```

### 4. **Criar Script de Atualização**
```python
# update_system.py
def update_system():
    # Backup automático
    # Atualização de arquivos
    # Verificação de integridade
    pass
```

## 🔄 Processo de Atualização Automática

### 1. **Script de Atualização**
```python
#!/usr/bin/env python3
import shutil
import os
from datetime import datetime

def backup_system():
    """Cria backup do sistema atual"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = [
        "app_catalogo_cursor.py",
        "provedores.json",
        "siglas.json",
        "palavras_remover.json"
    ]
    
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, backup_dir)
    
    print(f"✅ Backup criado: {backup_dir}")

def update_system():
    """Atualiza o sistema"""
    print("🔄 Iniciando atualização...")
    
    # 1. Backup
    backup_system()
    
    # 2. Atualizar arquivos
    # (aqui você adicionaria a lógica de atualização)
    
    # 3. Verificar integridade
    verify_system()
    
    print("✅ Sistema atualizado com sucesso!")

def verify_system():
    """Verifica se o sistema está funcionando"""
    try:
        import app_catalogo_cursor
        print("✅ Sistema verificado - OK")
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
```

### 2. **Atualização via Git (Recomendado)**
```bash
# Se usar controle de versão
git add .
git commit -m "Correção: [descrição do problema]"
git push origin main

# Para atualizar em outros computadores
git pull origin main
```

## 📋 Checklist de Correção

### Antes de Corrigir
- [ ] Identificar exatamente o problema
- [ ] Criar backup do sistema atual
- [ ] Isolar o problema em teste
- [ ] Documentar o comportamento esperado

### Durante a Correção
- [ ] Implementar correção gradual
- [ ] Testar cada mudança
- [ ] Adicionar logs para debug
- [ ] Tratar exceções adequadamente

### Após a Correção
- [ ] Testar com dados reais
- [ ] Verificar outras funcionalidades
- [ ] Atualizar documentação
- [ ] Criar script de atualização se necessário

## 🚀 Como Distribuir Correções

### 1. **Correção Simples**
- Atualizar apenas o arquivo principal
- Usuário substitui o arquivo antigo

### 2. **Correção com Dependências**
- Atualizar `requirements.txt`
- Usuário executa `pip install -r requirements.txt`

### 3. **Correção Completa**
- Criar novo instalador
- Usuário executa `instalar.bat` novamente

### 4. **Atualização Automática**
- Criar script `atualizar.bat`
- Usuário executa para atualização automática

## 📞 Suporte Técnico

### Informações Necessárias para Ajuda
1. **Descrição do problema**: O que não está funcionando?
2. **Mensagem de erro**: Qual erro aparece?
3. **Passos para reproduzir**: Como reproduzir o problema?
4. **Dados de teste**: Quais dados estão sendo usados?
5. **Versão do sistema**: Qual versão está usando?

### Exemplo de Relatório de Bug
```
PROBLEMA: Função de exportação não funciona
ERRO: "Permission denied" ao salvar arquivo
REPRODUZIR: 
1. Buscar peça
2. Clicar em "Exportar CSV"
3. Selecionar pasta
DADOS: ID da peça: 5042ecad-dbcb-92314cc6-2fb6-6b213869-a827
VERSÃO: v1.0
```

---
**Dica**: Sempre teste as correções em ambiente de desenvolvimento antes de distribuir! 