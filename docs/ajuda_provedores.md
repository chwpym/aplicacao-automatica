# 📚 Guia de Cadastro de Provedores de Dados

## 🎯 Visão Geral
Este guia explica como cadastrar diferentes tipos de provedores de dados no sistema de aplicações de peças.

## 📋 Tipos de Provedores Suportados

### 1. 🔗 **Provedores GraphQL**
Provedores que usam API GraphQL para buscar dados.

#### Exemplo: Authomix
```
Nome: Authomix
URL: https://bff.catalogofraga.com.br/gateway/graphql
Tipo: graphql
Origin: https://catalogo.authomix.com.br
Referer: https://catalogo.authomix.com.br/
```

#### Exemplo: Sabo
```
Nome: Sabo
URL: https://bff.catalogofraga.com.br/gateway/graphql
Tipo: graphql
Origin: https://catalogo.sabo.com.br
Referer: https://catalogo.sabo.com.br/
```

### 2. 🌐 **Provedores REST**
Provedores que usam APIs REST ou sites web que precisam de parsing HTML.

#### Exemplo: Nakata
```
Nome: Catálogo Nakata
URL: https://www.nakata.com.br/catalogo/aplicacao/{id}
Tipo: rest
Origin: https://www.nakata.com.br
Referer: https://www.nakata.com.br/
```

### 3. 💻 **Provedores Locais (Windows)**
Provedores instalados localmente no computador.

#### Exemplo: Catálogo Local
```
Nome: Meu Catálogo Local
URL: file:///C:/Programas/Catalogo/aplicacao.html?id={id}
Tipo: rest
Origin: file:///C:/Programas/Catalogo/
Referer: file:///C:/Programas/Catalogo/
```

## 📝 Instruções Detalhadas por Tipo

### 🔗 **GraphQL - Passo a Passo**

1. **Nome**: Digite um nome descritivo (ex: "Authomix", "Sabo")
2. **URL**: URL da API GraphQL (ex: https://bff.catalogofraga.com.br/gateway/graphql)
3. **Tipo**: Selecione "graphql"
4. **Origin**: URL de origem do catálogo (ex: https://catalogo.authomix.com.br)
5. **Referer**: URL de referência (ex: https://catalogo.authomix.com.br/)
6. **Ativo**: Marque se o provedor deve estar disponível

**Query GraphQL Padrão:**
```graphql
query GetProductById($id: String!, $market: MarketType!) {
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
}
```

### 🌐 **REST - Passo a Passo**

1. **Nome**: Digite um nome descritivo (ex: "Catálogo Nakata")
2. **URL**: URL com placeholder {id} (ex: https://www.nakata.com.br/catalogo/aplicacao/{id})
3. **Tipo**: Selecione "rest"
4. **Origin**: URL de origem do site
5. **Referer**: URL de referência
6. **Ativo**: Marque se o provedor deve estar disponível

**Observações para REST:**
- O sistema fará parsing HTML automaticamente
- Use {id} na URL para substituir pelo ID da peça
- O sistema extrairá informações usando regex

### 💻 **Local (Windows) - Passo a Passo**

1. **Nome**: Digite um nome descritivo (ex: "Meu Catálogo Local")
2. **URL**: Caminho local com placeholder {id} (ex: file:///C:/Programas/Catalogo/aplicacao.html?id={id})
3. **Tipo**: Selecione "rest"
4. **Origin**: Caminho local do programa
5. **Referer**: Caminho local do programa
6. **Ativo**: Marque se o provedor deve estar disponível

**Exemplos de Caminhos Locais:**
```
file:///C:/Programas/Catalogo/aplicacao.html?id={id}
file:///D:/Catálogos/MeuCatalogo/index.html?parte={id}
file:///C:/Users/SeuUsuario/Documents/Catalogo/aplicacao.php?id={id}
```

## 🔧 **Como Descobrir as Informações**

### Para Sites Web:
1. **Abra o site do catálogo**
2. **Pressione F12** para abrir as ferramentas do desenvolvedor
3. **Vá na aba Network**
4. **Faça uma busca no catálogo**
5. **Observe as requisições** para descobrir:
   - URL da API
   - Headers (Origin, Referer)
   - Tipo de requisição (GET/POST)

### Para Programas Locais:
1. **Abra o programa do catálogo**
2. **Verifique se ele abre no navegador** (HTML local)
3. **Anote o caminho** onde o programa está instalado
4. **Teste se consegue acessar** via file:///

## ⚠️ **Dicas Importantes**

1. **Teste sempre** após cadastrar um novo provedor
2. **Use IDs válidos** para testar
3. **Verifique se o site/programa está online**
4. **Para sites que mudam**, pode ser necessário atualizar as configurações
5. **Para programas locais**, certifique-se que o caminho está correto

## 🆘 **Solução de Problemas**

### Provedor não funciona:
- ✅ Verifique se a URL está correta
- ✅ Confirme se o Origin e Referer estão certos
- ✅ Teste se o site/programa está acessível
- ✅ Verifique se o tipo (graphql/rest) está correto

### Erro de conexão:
- ✅ Verifique sua conexão com a internet
- ✅ Confirme se o site não está bloqueado
- ✅ Teste se o programa local está funcionando

### Nenhum resultado encontrado:
- ✅ Use um ID válido de peça
- ✅ Verifique se o provedor está ativo
- ✅ Confirme se a estrutura de dados está correta

## 📞 **Suporte**

Se precisar de ajuda para cadastrar um provedor específico:
1. Anote o nome do catálogo/programa
2. Colete as informações da API/site
3. Teste primeiro com as instruções acima
4. Se não funcionar, entre em contato com suporte 