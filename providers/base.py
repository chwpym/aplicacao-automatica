class BaseProvider:
    def buscar(self, termo):
        raise NotImplementedError("Método buscar deve ser implementado pela subclasse.") 