class BaseProvider:
    """
    Classe base abstrata para provedores de dados.
    Todas as subclasses devem implementar o método 'buscar'.
    """
    def buscar(self, termo):
        raise NotImplementedError("Método buscar deve ser implementado pela subclasse.") 