# 💻 Guia de Provedores Locais

## 🎯 O que são Provedores Locais?

Provedores locais são programas ou catálogos instalados no seu computador Windows que podem fornecer informações sobre aplicações de peças automotivas.

## 📋 Tipos de Provedores Locais

### 1. **Executáveis (.exe)**
- Programas instalados no Windows
- Exemplo: `C:\Program Files\Catálogo Fraga\catalogo.exe`

### 2. **Arquivos HTML Locais**
- Catálogos em formato web local
- Exemplo: `file:///C:/Programas/Catalogo/aplicacao.html`

### 3. **Scripts Python**
- Scripts personalizados
- Exemplo: `python C:\Scripts\meu_catalogo.py`

## 🔧 Como Configurar um Provedor Local

### Passo 1: Abrir Gerenciador de Provedores
1. No menu principal: **Ações → Gerenciar Provedores**
2. Clique em **➕ Adicionar**

### Passo 2: Configurar Campos
```
Nome: Nome do seu catálogo local
URL: Caminho do executável ou arquivo
Tipo: local
Ativo: ✓ (marcado)
```

### Passo 3: Configurações Específicas
- **Executável**: Caminho completo do programa
- **Comando**: Comando para buscar (ex: `buscar {id}`)

### Passo 4: Testar
- Clique em **🧪 Testar Provedor**
- Verifique se funciona corretamente

## 📁 Exemplos de Configuração

### Exemplo 1: Catálogo Fraga Local
```
Nome: Catálogo Fraga Local
URL: C:\Program Files\Catálogo Fraga\catalogo.exe
Tipo: local
Executável: C:\Program Files\Catálogo Fraga\catalogo.exe
Comando: buscar {id}
```

### Exemplo 2: HTML Local
```
Nome: Meu Catálogo HTML
URL: file:///C:/Programas/Catalogo/aplicacao.html?id={id}
Tipo: rest
Origin: file:///C:/Programas/Catalogo/
Referer: file:///C:/Programas/Catalogo/
```

### Exemplo 3: Script Python
```
Nome: Script Personalizado
URL: python C:\Scripts\catalogo.py
Tipo: local
Executável: python
Comando: C:\Scripts\catalogo.py {id}
```

## 🔍 Como Descobrir Informações do Provedor Local

### Para Executáveis (.exe):
1. **Localizar o programa**:
   - Menu Iniciar → Programas
   - Clicar com botão direito → Abrir local do arquivo
   - Anotar o caminho completo

2. **Descobrir comandos**:
   - Abrir Prompt de Comando
   - Navegar até a pasta do programa
   - Executar: `nome_do_programa.exe --help`
   - Ou: `nome_do_programa.exe /?`

3. **Testar busca**:
   - Executar: `nome_do_programa.exe buscar ID_DA_PECA`
   - Verificar se retorna dados

### Para HTML Locais:
1. **Localizar arquivos**:
   - Procurar por arquivos `.html` na pasta do programa
   - Verificar se há arquivos de aplicação

2. **Testar URL**:
   - Abrir no navegador: `file:///C:/Caminho/para/arquivo.html?id=TESTE`
   - Verificar se carrega corretamente

### Para Scripts Python:
1. **Localizar script**:
   - Procurar por arquivos `.py`
   - Verificar se aceita parâmetros

2. **Testar execução**:
   - Prompt de Comando: `python script.py ID_DA_PECA`
   - Verificar saída

## 🧪 Testando Provedores Locais

### Teste Automático:
1. Menu: **Ações → 🔍 Testar Provedores Locais**
2. Sistema testa todos os provedores locais
3. Mostra resultados na tela

### Teste Manual:
1. **Gerenciar Provedores → 🧪 Testar Provedor**
2. Usa ID de teste: `5042ecad-dbcb-92314cc6-2fb6-6b213869-a827`
3. Verifica se retorna dados

## ⚠️ Solução de Problemas

### ❌ "Executável não encontrado"
**Solução:**
- Verificar se o caminho está correto
- Usar caminho completo (C:\...)
- Verificar se o arquivo existe

### ❌ "Permissão negada"
**Solução:**
- Executar como Administrador
- Verificar permissões da pasta
- Verificar se o antivírus não está bloqueando

### ❌ "Comando não reconhecido"
**Solução:**
- Verificar sintaxe do comando
- Testar no Prompt de Comando primeiro
- Verificar se o programa aceita parâmetros

### ❌ "Nenhum resultado"
**Solução:**
- Verificar se o ID é válido
- Testar com ID conhecido
- Verificar formato de saída do programa

## 📝 Formatos de Saída Esperados

### Para Executáveis:
O programa deve retornar dados em formato texto ou JSON:
```
Marca: FORD
Modelo: FIESTA
Ano: 2010-2015
Motor: 1.0
```

### Para HTML:
O arquivo deve conter tabelas ou dados estruturados:
```html
<table>
  <tr><td>Marca</td><td>FORD</td></tr>
  <tr><td>Modelo</td><td>FIESTA</td></tr>
</table>
```

### Para Scripts Python:
O script deve imprimir dados no console:
```python
print("Marca: FORD")
print("Modelo: FIESTA")
print("Ano: 2010-2015")
```

## 🔄 Atualizando Provedores Locais

### Quando Atualizar:
- Programa foi reinstalado
- Caminho mudou
- Comandos mudaram
- Versão nova do catálogo

### Como Atualizar:
1. **Gerenciar Provedores**
2. Selecionar provedor na lista
3. **✏️ Atualizar Selecionado**
4. Modificar campos necessários
5. **🧪 Testar Provedor**
6. **💾 Salvar e Fechar**

## 📊 Provedores Comuns Detectados

O sistema pode detectar automaticamente:
- **Catálogo Fraga**: `C:\Program Files\Catálogo Fraga\`
- **Authomix Local**: `C:\Program Files\Authomix\`
- **Sabo Local**: `C:\Program Files\Sabo\`

## 🆘 Suporte

Se encontrar problemas:
1. Verificar se o programa está funcionando
2. Testar comandos manualmente
3. Verificar permissões de arquivo
4. Consultar documentação do programa

---
**Dica**: Sempre teste o provedor local antes de usar no sistema principal! 