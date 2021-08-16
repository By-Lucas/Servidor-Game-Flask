
#CLASSE A SER IMPORTADA PELOS MODULOS jogoteca e dao
class Jogo: #CRIANDO UMA CLASSE PARA O SERVIDOR, CRIANDO O SERVIDOR
    def __init__(self, nome, categoria, console, id=None): #INFORMACOES QUE TEM NO SERVIDOR
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha