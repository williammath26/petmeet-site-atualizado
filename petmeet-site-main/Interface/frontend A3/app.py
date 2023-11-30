from flask import Flask, render_template, request, redirect, session
import jwt
import requests

app = Flask(__name__)
app.secret_key = '123456'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    # Envie os dados de login para a sua API usando requests
    login_url = 'http://127.0.0.1:5000/users/login'
    response = requests.post(login_url, json={'Email': email, 'Senha': senha})

    if response.ok:
        user_data = response.json()
        access_token = user_data.get('access_token')
        user_name = user_data.get('user_name')  # Adicione esta linha para obter o nome do usuário
        if access_token and user_name:
            # Restante do código...
            return render_template('main.html', user_name=user_name)
        else:
            return 'Invalid response from server.'

# Adicione uma rota para a página 'main.html'
@app.route('/main')
def main():
    user_name = session.get('user_name')
    return render_template('main.html', user_name=user_name)

@app.route('/cadastro', methods=['POST'])
def cadastro():
    # Obtendo dados do formulário
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email_or_phone = request.form['email_or_phone']
    new_password = request.form['new_password']

    # Montando payload para enviar à API
    payload = {
        'Nome': f"{first_name} {last_name}",
        'Email': email_or_phone,
        'Senha': new_password,
    }

    # Enviando solicitação à API
    api_url = 'http://127.0.0.1:5000/users/create'
    response = requests.post(api_url, json=payload)

    if response.status_code == 201:
        user_data = response.json()
        user_id = user_data.get('ID')
        return f'<script>hide(); alert("Successfully registered! User ID: {user_id}");</script>'
    else:
        # Tratamento de erro, você pode renderizar uma página de erro, por exemplo.
        return 'Error during registration.'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
