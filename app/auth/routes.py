from flask import Blueprint, request, jsonify, current_app
from app import db
from datetime import datetime
from app.models.users import Usuario
from werkzeug.security import generate_password_hash
from app.utils.validator import validar_senha, validar_email, validar_nome, validar_data_nascimento

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/criar_conta', methods=['POST'])
def registrar():
    """
    Registrar um novo usuário no sistema.

    Espera receber:
    - nome: Nome completo do usuário
    - email: Email válido e único
    - senha: Senha que atende aos requisitos mínimos
    - repetir_senha: Confirmação da senha
    - data_nascimento: Data no formato DD-MM-YYYY

    Retorna:
    - Sucesso: {'mensagem: 'Usuario registrado com sucesso}, 201
    - Erro de validação: {'erros': [lista de erros]}, 400
    - Erro interno: {'erros': ['mensagem de erro']}, 500
    """

    try:
        
        current_app.logger.info(f"Dados recebidos: {request.form}")

        nome = request.form.get("nome")
        email = request.form.get("email")
        data_de_nascimento = request.form.get("data_nascimento")
        senha = request.form.get("senha")
        repetir_Senha = request.form.get("repetir_senha")

        

        erros = []

        nome_erros = validar_nome(nome) or []
        email_erros = validar_email(email) or []
        data_erros = validar_data_nascimento(data_de_nascimento) or []
        senha_erros = validar_senha(senha) or []

        erros.extend(nome_erros)
        erros.extend(email_erros)
        erros.extend(data_erros)
        
        if senha != repetir_Senha:
            erros.append('A senha e a confirmação devem ser idênticas')
            
        erros.extend(senha_erros)

        email_existente = Usuario.query.filter_by(email=email).first()
        
        if email_existente:
            erros.append('E-mail já cadastrado')

        if erros:
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
            current_app.logger.error(f'Erro ao salvar usuário. Detalhes: {str(e)}')
            current_app.logger.error(f'Dados recebidos: {nome}, {email}, {data_de_nascimento}')
            return jsonify({'erros': ['Erro ao salvar usuário']}), 500

        return jsonify({'mensagem': 'Usuario registrado com sucesso'}), 201
    
    except Exception as e:
        current_app.logger.error(f'Erro interno no servidor: {str(e)}')
        return jsonify({'erros': ['Erro interno no servidor']}), 500    