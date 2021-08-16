from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
import time

from models import Jogo
from dao import JogoDao, UsuarioDao

from helpers import deleta_arquivo, recupera_imagem
from jogoteca import db, app

jogo_dao = JogoDao(db) #VARIAVEL BANCO DE DADOS JOGO
usuario_dao = UsuarioDao(db)  #VARIAVEL BANCO DE DADOS USUARIO



@app.route('/inicio') #CRIAR PAGINA "inicio"
def index():
    lista = jogo_dao.listar() #criar variavel para listar os jogos cadastrados no db
    return render_template('lista.html', titulo='Servidor ADM', jogos=lista) #EXECUTAR janela inicio e mostrar nos jogos


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
        
    #O CODIGO ABAIXO FOI SUBSTITUIDO PELO CODIGO ACIMA, ESTE ABAIXO SÓ LOGA COM A SENHA MESTRA E O ACIMA COM USUAIOOS CADASTRADOS
        ''' if 'mestra' == request.form['senha']:  #O CLIENTE SÓ SERÁ AUTENTICADO SE ELE COLOCAR A SENHA 'mestra'
        session ['usuario_logado'] = request.form['usuario'] #PARA TER VARIOS USUARIOS LOGADO
        flash(request.form['usuario'] + ', logou com sucesso!') #FUNCAO PARA CHAMAR O NOME DO USUARIO NO template.html e MOSTRAR A MENSAGEL DE LOGADOS
        #return redirect('/inicio') #SE A SENHA TIVER CORRETA ELE VAI PARA A PAGINA DE LOGIN
        proxima_pagina =  request.form['proxima']
        return redirect(proxima_pagina)  #REDIRECIONA PARA A PGINA QUE EU QUERO APÓS ESTA
        '''
    
    else: #SE A SENHA ESTIVER ERRADA ELE VAI PARA A PAGINA ABAIXO
        flash('Não logado, tente novamente! Fale com Administrador Whatsapp 74981199190')
        return redirect(url_for('login'))#SE A SENHA ESTIVER ERRADA ELE VAI PARA A PAGINA "inicio"


@app.route('/logout') #PARA MOSTRAR MENSAGEM SE TEM ALGUM USUARIO LOGADO OU NAO
def logout():
    session['usuario_logado'] = None
    flash('Voce saiu, nenhum usuario logado!')
    return redirect(url_for('index')) #REDIRECIONA PARA A PGINA QUE EU QUERO APÓS ESTA

@app.route('/uploads/<nome_arquivo>') #MOSTRAR IMAGEM NA TELA DE CADASTRAR NOVO JOGO
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
