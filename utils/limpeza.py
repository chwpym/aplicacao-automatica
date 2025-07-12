# Funções de limpeza de texto serão movidas para cá 
 
def remover_palavras_avancado(texto, palavras_remover):
    """Remove palavras/frases do texto conforme lista fornecida."""
    for palavra in palavras_remover:
        texto = texto.replace(palavra, "")
    return texto 