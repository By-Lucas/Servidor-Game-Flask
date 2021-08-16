from datetime import time
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
import MySQLdb
from models import Jogo, Usuario
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL
from flask.helpers import flash
import os
import time

'''print('Conectando...') #SE O MYSQL ESTIVER PRONTO, VAI APARECER ESTA MENSAGEM'''
#MODELO DE MYSQL DO CURSO ABAIXO
'''conn = MySQLdb.connect(user='root', passwd='', host='localhost', port=3306)'''


app = Flask(__name__)
app.secret_key = 'lucas' #SÓ TEM A LEITURA DE SENHAS E USUARIOS SE ESTIVER ESE CODIGO SECRETO

#IMPORTAR AS CONFIGURACOES DO MYSQL "dao" E SALVAR NO DAO( OU QUER DIZER, BANCO DE DADOS)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'  #NOME DO CAMINHO ONDE VAI SALVAR TODOS OS UPLOADS
db = MySQL(app) #RODAR O BANCO DE DADOS 

jogo_dao = JogoDao(db) #VARIAVEL BANCO DE DADOS JOGO
usuario_dao = UsuarioDao(db)  #VARIAVEL BANCO DE DADOS USUARIO



@app.route('/inicio') #CRIAR PAGINA "inicio"
def index():
    lista = jogo_dao.listar() #criar variavel para listar os jogos cadastrados no db
    return render_template('lista.html', titulo='Cadastros', jogos=lista) #EXECUTAR janela inicio e mostrar nos jogos


@app.route('/novo') #CRIAR PAGINA "novo" PARA CADASTRAR NOVO JOGO E SÓ TER ACESSO SE STIVER LOGADO
def novo():
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo'))) #DEPOIS DE LOGAR ELE VAI SEGUIR O CAMINHO QUE QUERO, QUE É A TELA DE CADASTRO DE JOGOS
    return render_template('novo.html', titulo='Novo Jogo') 
    

@app.route('/criar', methods=['POST',]) #CRIAR JOGO NOVO "criar" no formato de POST para poder adcionar informaceos
def criar():  #CODIGO PARA CRIAR CADASTRAR OS JOGOS 
    nome = request. form['nome']
    categoria = request. form['categoria']
    console = request. form['console']
    jogo = Jogo(nome, categoria, console)
    jogo  = jogo_dao.salvar(jogo)
    
    arquivo = request.files['arquivo'] #CARREGAR UMA IMAGEM PARA O JOGO
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg') # ONDE SALVAR A IMAGEM CARREGADA COM O NOME O id do jogo
    return redirect(url_for('index')) #REDIRECIONA PARA A PAGINA DO "inicio" APOS CADASTRAR UM JOGO PARA NAO FICAR SÓ CADASTRANDO QUANDO ATUALIZAR A PAGINA


@app.route('/editar/<int:id>') #CRIAR PAGINA "novo" PARA CADASTRAR NOVO JOGO E SÓ TER ACESSO SE STIVER LOGADO
def editar(id):
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar'))) #DEPOIS DE LOGAR ELE VAI SEGUIR O CAMINHO QUE QUERO, QUE É A TELA DE CADASTRO DE JOGOS
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id) #CODIGO PARA ALTERAR A IMAGEM NO EDITAR 
    capa_jogo = f'capa{id}.jpg'
    return render_template('editar.html', titulo='Editando jogo', jogo=jogo, capa_jogo = nome_imagem) #MOSTRAR IMAGEM DO JOGO EM EDITAR
   

@app.route('/atualizar', methods=['POST',]) #CRIAR JOGO NOVO "criar" no formato de POST para poder adcionar informaceos
def atualizar():  #CODIGO PARA CRIAR CADASTRAR OS JOGOS 
    nome = request. form['nome']
    categoria = request. form['categoria']
    console = request. form['console']
    jogo = Jogo(nome, categoria, console, id = request.form['id'])
    jogo_dao.salvar(jogo)
    
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>') #PARA DELETAR POR ID DO PRODUTO
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!') #printar mensagem na tela
    return redirect(url_for('index'))


#PAGINA DE CADASTRO DE USUARIO
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima) #DADOS QUE VAI SER SALVO NO FORMULARIOS DE LOGIN


#AUTENTICANDO CADASRTO
@app.route('/autenticar', methods =['POST',])
def autenticar(): #ESSA FUNCAO SERVE PARAO CLIENTE SE CADASTRAR
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!') #FUNCAO PARA CHAMAR O NOME DO USUARIO NO template.html e MOSTRAR A MENSAGEM DE LOGADOS PARA OUTROS USUARIOS TAMBEM
            proxima_pagina =  request.form['proxima']
            return redirect(proxima_pagina)
        
    else: #SE A SENHA ESTIVER ERRADA ELE VAI PARA A PAGINA ABAIXO
        flash('Não logado, tente novamente! Fale com Administrador Whatsapp 74981199190')
        return redirect(url_for('login'))#SE A SENHA ESTIVER ERRADA ELE VAI PARA A PAGINA "inicio"


@app.route('/logout') #PARA MOSTRAR MENSAGEM SE TEM ALGUM USUARIO LOGADO OU NAO
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuario logado!')
    return redirect(url_for('login')) #REDIRECIONA PARA A PGINA QUE EU QUERO APÓS ESTA


@app.route('/uploads/<nome_arquivo>') #MOSTRAR IMAGEM NA TELA DE CADASTRAR NOVO JOGO
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))


#debug=True  # SERVE PARA QUANDO SALVAR O CODIGO ELE INICIAR AUTOMATICAMENTE SEM PRECISAR RESTARTAR
app.run(host='localhost', port=3631, debug=True)        # trecho da app para rodar o ambiente no meu endereço IP