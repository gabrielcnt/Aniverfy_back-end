from flask import Blueprint, request, jsonify
from logger import criar_logger
from app import db
from datetime import datetime
from app.models.users import Usuario
from werkzeug.security import generate_password_hash
from app.utils.validator import validar_senha, validar_email, validar_nome, validar_data_nascimento

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

register_log = criar_logger('Register')

@auth_bp.route('/criar_conta', methods=['POST'])
def registrar():
    """
    Registrar um novo usuário no sistema.

    Espera receber:
    - nome: Nome completo do usuário
    - email: Email válido e único
    - senha: Senha que atende aos requisitos mínimos
    - data_nascimento: Data no formato DD-MM-YYYY

    Retorna:
    - Sucesso: {'mensagem: 'Usuario registrado com sucesso}, 201
    - Erro de validação: {'erros': [lista de erros]}, 400
    - Erro interno: {'erros': ['mensagem de erro']}, 500
    """

    try:
        register_log.info('Iniciando processo de registro')
        register_log.debug("Método da requisição: {request.method}")
        nome = request.form.get("nome")
        email = request.form.get("email")
        data_de_nascimento = request.form.get("data_nascimento")
        senha = request.form.get("senha")
        
        register_log.info(f"Dados recebidos: {request.form}")

        erros = []

        nome_erros = validar_nome(nome) or []
        email_erros = validar_email(email) or []
        data_erros = validar_data_nascimento(data_de_nascimento) or []
        senha_erros = validar_senha(senha) or []

        erros.extend(nome_erros)
        erros.extend(email_erros)
        erros.extend(data_erros)
        
            
        erros.extend(senha_erros)

        email_existente = Usuario.query.filter_by(email=email).first()
        
        if email_existente:
            register_log.debug('Tentativa de cadastrar um email que ja esta no banco de dados')
            erros.append('E-mail já cadastrado')

        if erros:
            register_log.error("erros de validação encontrados: {erros}")
            return jsonify({'erros': erros}), 400
        
        password_hash = generate_password_hash(senha)
        data_de_nascimento_obj = datetime.strptime(data_de_nascimento, '%d-%m-%Y').date()
        try:
            new_user = Usuario(
            name=nome,
            email=email, 
            password_hash=password_hash,
            data_nascimento=data_de_nascimento_obj
            )
            
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            register_log.error(f'Erro ao salvar usuário. Detalhes: {str(e)}')
            register_log.error(f'Dados recebidos: {nome}, {email}, {data_de_nascimento}')
            return jsonify({'erros': ['Erro ao salvar usuário']}), 500

        return jsonify({'mensagem': 'Usuario registrado com sucesso'}), 201
    
    except Exception as e:
        register_log.error(f'Erro interno no servidor: {str(e)}')
        return jsonify({'erros': ['Erro interno no servidor']}), 500
