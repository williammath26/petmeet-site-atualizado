from flask import request
import jwt
from datetime import datetime, timedelta


SECRET_KEY = '123456'


def check_jwt_token():
    global user_token
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        if is_valid_token(token):
            user_token = token


# Função para verificar se o token JWT é válido
def is_valid_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False  # Token expirado
    except jwt.InvalidTokenError:
        return False  # Token inválido


# Variável global para armazenar o token JWT após o login
user_token = None

# Função para gerar um token JWT


def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token válido por 1 dia
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Função para verificar e decodificar um token JWT


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

# Decorador personalizado para verificar a autenticação com JWT


def jwt_auth_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return {'message': 'Token is missing'}, 401

        token = token.split('Bearer ')[-1]

        payload = decode_token(token)
        if payload is None:
            return {'message': 'Token is invalid or expired'}, 401

        return func(payload, *args, **kwargs)

    return wrapper
