import requests
from bs4 import BeautifulSoup, Tag
from typing import cast

class ATEProvider:
    BASE_URL = "https://catalogoexpresso.com.br/ATE/detalhes.php"

    def get_detalhes(self, cw_filtros, cw_ie_tp, cw_produtoAtivo, timeout=20):
        """
        Busca detalhes no catálogo ATE.
        Args:
            cw_filtros (str): Filtros para a query (ex: 'PCs<!2!>6013')
            cw_ie_tp (int): Tipo IE (ex: 0)
            cw_produtoAtivo (str): Produto ativo (ex: 'CodigoProduto<!2!>2497')
            timeout (int): Timeout da requisição em segundos
        Returns:
            str: HTML retornado pelo servidor
        """
        params = {
            'cw_filtros': cw_filtros,
            'cw_ie_tp': cw_ie_tp,
            'cw_produtoAtivo': cw_produtoAtivo
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': 'https://catalogoexpresso.com.br/ATE/resultado.php',
        }
        response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text

    @staticmethod
    def buscar_produto(html):
        """
        Recebe o HTML da página de detalhes e retorna uma lista de aplicações estruturadas no formato padrão do sistema.
        Args:
            html (str): HTML da página de detalhes do produto ATE
        Returns:
            list[dict]: Lista de aplicações no formato padrão
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = []
        table = soup.find('table', class_='align-content-between')
        if not isinstance(table, Tag):
            return result
        current_montadora = None
        for tr in table.find_all('tr'):
            if not isinstance(tr, Tag):
                continue
            th = tr.find('th', class_='tituloMontadora') if isinstance(tr, Tag) else None
            if isinstance(th, Tag):
                current_montadora = th.get_text(strip=True)
                continue
            tr_classes = tr.get('class') if isinstance(tr, Tag) else None
            if not isinstance(tr_classes, list):
                tr_classes = []
            if 'ideia-linha-aplicacao' in tr_classes:
                tds = tr.find_all('td', class_='tituloAplicacao') if isinstance(tr, Tag) else []
                if not tds or len(tds) < 4:
                    continue
                veiculo = tds[0].get_text(strip=True)
                modelo = ''
                if len(tds) > 1 and isinstance(tds[1], Tag):
                    modelo_div = cast(Tag, tds[1]).find('div')
                    if isinstance(modelo_div, Tag) and 'conteudo' in (modelo_div.get('class') or []):
                        modelo = modelo_div.get_text(strip=True)
                versao = ''
                if len(tds) > 2 and isinstance(tds[2], Tag):
                    versao_div = cast(Tag, tds[2]).find('div')
                    if isinstance(versao_div, Tag) and 'conteudo' in (versao_div.get('class') or []):
                        versao = versao_div.get_text(strip=True)
                ano = ''
                if len(tds) > 3 and isinstance(tds[3], Tag):
                    ano_div = cast(Tag, tds[3]).find('div')
                    if isinstance(ano_div, Tag) and 'conteudo' in (ano_div.get('class') or []):
                        ano = ano_div.get_text(strip=True)
                abs_ = ''
                if len(tds) > 4 and isinstance(tds[4], Tag):
                    abs_div = cast(Tag, tds[4]).find('div')
                    if isinstance(abs_div, Tag) and 'conteudo' in (abs_div.get('class') or []):
                        abs_ = abs_div.get_text(strip=True)
                # Adaptação para o formato padrão do sistema
                start_year = ano.split('-')[0].strip() if ano else ''
                end_year = ano.split('-')[1].strip() if ano and '-' in ano else ''
                # Só adiciona se veiculo e current_montadora estiverem preenchidos
                if veiculo and current_montadora:
                    result.append({
                        'brand': current_montadora,
                        'name': veiculo,
                        'model': modelo,
                        'engineName': versao,
                        'engineConfiguration': '',
                        'brakeSystem': abs_,
                        'startYear': start_year,
                        'endYear': end_year,
                        'note': '',
                        'only': '',
                        'restriction': ''
                    })
        return result
