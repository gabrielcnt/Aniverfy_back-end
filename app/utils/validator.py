import re
from flask import jsonify
from datetime import datetime

def validar_nome(name: str) -> list:
    erros = []
    if not name:
        erros.append('campo Nome Completo é obrigatório')
    return erros



def validar_email(email: str) -> list:

    erros = []
    
    if not email:
        erros.append('Campo E-mail é obrigatório')        
        return erros
    
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(padrao, email):
        erros.append('Email invalido')
        return erros



def validar_data_nascimento(data: str) -> list:
    erros = []
    if not data:
        erros.append('Data de nascimento é obrigatória')
        return erros
    
    try:
        datetime.strptime(data, '%d-%m-%Y')
    except ValueError:
        erros.append('Data de nascimento inválida')
    return erros



def validar_senha(senha: str) -> list:

    erros = []

    if not senha:
        erros.append('O campo Senha é obrigatório')
        return erros
    

    if len(senha) < 8:
        erros.append("A senha deve ter pelo menos 8 caracteres")
        
    if not re.search(r"[A-Z]", senha):
        erros.append("A senha deve ter pelo menos uma letra maiúscula")
    
    if not re.search(r"[a-z]", senha):
        erros.append("A senha deve ter pelo menos uma letra minúscula")
    
    if not re.search(r"[0-9]", senha):
        erros.append("A senha deve ter pelo menos um número")
    
    if not re.search(r"[@$!%*?&]", senha):
        erros.append("a senha deve ter pelo menos um caractere especial")
    
    if senha.lower() in ["123456", "senha", "admin", "qwerty"]:
        erros.append("A senha é muito fraca, coloque uma senha mais forte")
    
    return erros

