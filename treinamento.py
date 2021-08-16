from flask import Flask

#======= CODIGO PARA RODAR SERVIDOR FLASK ==========================================
app = Flask(__name__)     #Cria a classe

@app.route("/")           #Cria  rota 
def index():              #Faz aparecer o nome abaixo na tela
    return "OLA PESSOAL"  #Nome printado na tela

if __name__ == '__main__':#O main será o mesmo que name
    app.run(debug=True)   #Para rodar o servidor e alto restart quando salva
#====================================================================================






