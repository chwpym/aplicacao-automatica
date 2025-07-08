from .base import BaseProvider
import os
import pdfplumber

class PDFProvider(BaseProvider):
    """
    Provedor para busca de códigos em arquivos PDF.
    Implementa o método 'buscar' para localizar códigos em PDFs de uma pasta.
    """
    def buscar(self, termo, pasta='catalogos_pdf'):
        resultados = []
        for arquivo in os.listdir(pasta):
            if arquivo.lower().endswith('.pdf'):
                caminho_pdf = os.path.join(pasta, arquivo)
                try:
                    with pdfplumber.open(caminho_pdf) as pdf:
                        for i, page in enumerate(pdf.pages):
                            text = page.extract_text()
                            if not text:
                                continue
                            for linha in text.split('\n'):
                                if termo.upper() in linha.upper():
                                    resultados.append({
                                        'arquivo': arquivo,
                                        'pagina': i+1,
                                        'linha': linha.strip()
                                    })
                except Exception as e:
                    print(f"Erro ao ler {arquivo}: {e}")
        return resultados

    def buscar_em_pdfs_especificos(self, termo, pdfs, pasta='catalogos_pdf'):
        """
        Busca o termo apenas nos arquivos PDF especificados.
        :param termo: Código/termo a buscar
        :param pdfs: Lista de nomes de arquivos PDF
        :param pasta: Pasta onde estão os PDFs
        :return: Lista de dicionários com resultados
        """
        resultados = []
        for arquivo in pdfs:
            caminho_pdf = os.path.join(pasta, arquivo)
            try:
                with pdfplumber.open(caminho_pdf) as pdf:
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if not text:
                            continue
                        for linha in text.split('\n'):
                            if termo.upper() in linha.upper():
                                resultados.append({
                                    'arquivo': arquivo,
                                    'pagina': i+1,
                                    'linha': linha.strip()
                                })
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")
        return resultados 