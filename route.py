import os
import sys

# Garante caminhos absolutos corretos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'app', 'static')
MODELS_DIR = os.path.join(BASE_DIR, 'app', 'models')

for p in [BASE_DIR, MODELS_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=STATIC_DIR)

@app.route('/helper')
def helper(info=None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/')
@app.route('/portal')
def portal():
    aba = request.query.get('aba', 'adicionar')
    return ctl.portal(aba=aba)

@app.route('/portal', method='POST')
def portal_login():
    login = request.forms.get('login') or request.forms.get('usuario')
    senha = request.forms.get('senha')
    return ctl.autenticar(login, senha)

@app.route('/portal/adicionar', method='POST')
def portal_adicionar():
    nome_aluno = request.forms.get('nome_aluno')
    opcao_tipo = request.forms.get('opcao_tipo')
    data_aula = request.forms.get('data_aula')
    return ctl.adicionar_aluno(nome_aluno, opcao_tipo, data_aula)

@app.route('/portal/salario', method=['GET', 'POST'])
def portal_salario():
    if request.method == 'POST':
        tem_vt = request.forms.get('tem_vt')
        return ctl.calcular_salario(tem_vt)
    return ctl.portal(aba='salario')

@app.route('/portal/alterar', method=['GET', 'POST'])
def portal_alterar():
    if request.method == 'POST':
        indice = request.forms.get('indice')
        novo_nome = request.forms.get('novo_nome')
        nova_data = request.forms.get('nova_data')
        nova_opcao = request.forms.get('nova_opcao')
        return ctl.alterar_aluno(indice, novo_nome, nova_data, nova_opcao)
    return ctl.portal(aba='alterar')

@app.route('/portal/fim-do-mes', method='POST')
def portal_fim_do_mes():
    return ctl.finalizar_mes()

@app.route('/sair')
def sair():
    return ctl.sair()

#-----------------------------------------------------------------------------

if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True, reloader=True)
