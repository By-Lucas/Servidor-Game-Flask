from flask import Flask
from flask_mysqldb import MySQL
import os



'''print('Conectando...') #SE O MYSQL ESTIVER PRONTO, VAI APARECER ESTA MENSAGEM'''
#MODELO DE MYSQL DO CURSO ABAIXO
'''conn = MySQLdb.connect(user='root', passwd='', host='localhost', port=3306)'''


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = MySQL(app) #RODAR O BANCO DE DADOS 

from views import *

if __name__ == '__main__':
#debug=True  # SERVE PARA QUANDO SALVAR O CODIGO ELE INICIAR AUTOMATICAMENTE SEM PRECISAR RESTARTAR
    app.run(host='localhost', port=3631, debug=True)        # trecho da app para rodar o ambiente no meu endereço IP