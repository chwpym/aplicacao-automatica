# Como Adicionar um Novo Servidor

Este guia explica como adicionar um novo servidor/provedor ao sistema de catálogos de peças.

## 🚀 Métodos Disponíveis

### 1. Script Automatizado (Recomendado)

Execute o script `adicionar_servidor_simples.py`:

```bash
python3 adicionar_servidor_simples.py
```

#### Opções do Script:
- **Opção 1**: Adicionar novo servidor (interativo)
- **Opção 2**: Listar servidores existentes
- **Opção 3**: Adicionar servidor de exemplo
- **Opção 4**: Sair

### 2. Interface Gráfica

1. Execute a aplicação principal: `python3 src/app_catalogo.py`
2. No menu **Ações** → **Gerenciar Provedores**
3. Preencha os campos e clique em **Adicionar**

### 3. Edição Manual do JSON

Edite diretamente o arquivo `provedores.json`.

## 📋 Tipos de Servidor Suportados

### GraphQL
Para APIs GraphQL (como Authomix, Sabo, etc.):
```json
{
    "nome": "Meu Provedor GraphQL",
    "url": "https://api.meusite.com/graphql",
    "tipo": "graphql",
    "ativo": true,
    "headers": {
        "origin": "https://catalogo.meusite.com",
        "referer": "https://catalogo.meusite.com/"
    },
    "query": "query GetProductById($id: String!, $market: MarketType!) { ... }"
}
```

### REST
Para APIs REST (como Nakata, Wega, etc.):
```json
{
    "nome": "Meu Provedor REST",
    "url": "https://api.meusite.com/produtos/{id}",
    "tipo": "rest",
    "ativo": true,
    "headers": {
        "origin": "https://www.meusite.com",
        "referer": "https://www.meusite.com/",
        "User-Agent": "Mozilla/5.0 ...",
        "Accept": "application/json"
    },
    "query": ""
}
```

### Provedores Especiais
Para sistemas específicos:
```json
{
    "nome": "Meu Sistema Custom",
    "tipo": "meu_sistema",
    "ativo": true,
    "configuracao_especial": "valor"
}
```

## 🔧 Como Descobrir Informações de um Site

### 1. Usando Ferramentas do Desenvolvedor (F12)

1. **Abra o site do catálogo**
2. **Pressione F12** para abrir as ferramentas
3. **Vá na aba "Network" (Rede)**
4. **Faça uma busca** no catálogo
5. **Observe as requisições** para descobrir:
   - URL da API
   - Headers necessários (Origin, Referer)
   - Tipo de requisição (GET/POST)
   - Estrutura da query GraphQL (se aplicável)

### 2. Exemplos de Headers Importantes

```
Origin: https://catalogo.exemplo.com
Referer: https://catalogo.exemplo.com/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json, text/html
```

## 📊 Estrutura Completa do Provedor

```json
{
    "chave_unica": {
        "nome": "Nome Amigável",
        "url": "https://api.exemplo.com/endpoint/{id}",
        "tipo": "graphql|rest|local|custom",
        "ativo": true|false,
        "headers": {
            "origin": "https://site.com",
            "referer": "https://site.com/",
            "User-Agent": "...",
            "Accept": "...",
            "Authorization": "Bearer token" // se necessário
        },
        "query": "Query GraphQL ou string vazia para REST",
        "configuracoes_extras": {
            // Configurações específicas do provedor
        }
    }
}
```

## ✅ Exemplo Completo: Adicionando Manualmente

1. **Abra o arquivo `provedores.json`**
2. **Adicione a nova entrada antes do `}`:**

```json
    "meu_novo_provedor": {
        "nome": "Meu Catálogo",
        "url": "https://api.meucatalogo.com/buscar/{id}",
        "tipo": "rest",
        "ativo": true,
        "headers": {
            "origin": "https://www.meucatalogo.com",
            "referer": "https://www.meucatalogo.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        },
        "query": ""
    }
```

3. **Salve o arquivo**
4. **Reinicie a aplicação**

## 🧪 Testando o Novo Provedor

### Na Aplicação Principal:
1. Abra o **Gerenciador de Provedores**
2. Selecione seu provedor
3. Clique em **🧪 Testar Provedor**

### Script de Teste:
```bash
# Lista todos os provedores
python3 adicionar_servidor_simples.py
# Escolha opção 2
```

## ⚠️ Solução de Problemas

### Provedor não funciona:
- ✅ Verifique se a URL está correta
- ✅ Confirme se Origin e Referer estão corretos
- ✅ Teste se o site está acessível
- ✅ Verifique se o tipo (graphql/rest) está correto

### Erro de conexão:
- ✅ Verifique conexão com internet
- ✅ Confirme se o site não está bloqueado
- ✅ Verifique se precisa de autenticação

### Nenhum resultado:
- ✅ Use um ID válido de peça
- ✅ Verifique se o provedor está ativo
- ✅ Confirme a estrutura da resposta da API

## 📝 Exemplos de Provedores Existentes

### GraphQL (Authomix):
```json
{
    "nome": "Authomix",
    "url": "https://bff.catalogofraga.com.br/gateway/graphql",
    "tipo": "graphql",
    "ativo": true,
    "headers": {
        "origin": "https://catalogo.authomix.com.br",
        "referer": "https://catalogo.authomix.com.br/"
    },
    "query": "query GetProductById($id: String!, $market: MarketType!) { ... }"
}
```

### REST (Nakata):
```json
{
    "nome": "Catálogo Nakata",
    "url": "https://www.catalogonakata.com.br/detalhe/{id}",
    "tipo": "rest",
    "ativo": true,
    "headers": {
        "origin": "https://www.catalogonakata.com.br",
        "referer": "https://www.catalogonakata.com.br/detalhe/{id}",
        "User-Agent": "Mozilla/5.0 ..."
    },
    "query": ""
}
```

### Sistema Custom (Viemar):
```json
{
    "nome": "Viemar",
    "tipo": "viemar",
    "ativo": true
}
```

## 🎯 Dicas Importantes

1. **Use chaves únicas**: A chave do provedor deve ser única (ex: `meu_catalogo`)
2. **Headers corretos**: Origin e Referer são essenciais para APIs web
3. **URL com placeholder**: Use `{id}` onde o ID da peça será inserido
4. **Teste sempre**: Use a função de teste antes de usar em produção
5. **Backup**: Faça backup do `provedores.json` antes de editar

## 📞 Suporte

Se tiver dúvidas:
1. Consulte a documentação em `docs/`
2. Use o menu **Ajuda** na aplicação
3. Execute `python3 adicionar_servidor_simples.py` para assistência interativa

---

**✨ Pronto!** Agora você pode adicionar novos servidores ao sistema de catálogos!