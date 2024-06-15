from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from api.db_operations_api import get_engine, fetch_area_colhida, fetch_produtividade, fetch_quantidade_produzida

bp = Blueprint('api', __name__)

@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'msg': 'Missing username or password'}), 400

    # Exemplo de verificação simples, substitua pelo seu método de verificação de usuário
    if username == 'admin' and password == 'admin':  # Substitua por uma verificação real
        access_token = create_access_token(identity={'username': username})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'msg': 'Bad username or password'}), 401

@bp.route('/area_colhida', methods=['GET'])
def area_colhida():
    municipio_id = request.args.get('municipio_id')
    year = request.args.get('year')
    if not municipio_id or not year:
        return jsonify({'success': False, 'data': None, 'message': 'Parâmetros obrigatórios: municipio_id, year'}), 400
    engine = get_engine()  # Chamada sem o argumento 'context'
    data = fetch_area_colhida(engine, municipio_id, year)
    if data:
        return jsonify({'success': True, 'data': data, 'message': 'Dados recuperados com sucesso'})
    else:
        return jsonify({'success': False, 'data': None, 'message': 'Nenhum dado encontrado'}), 404

@bp.route('/produtividade', methods=['GET'])
def produtividade():
    estados = request.args.getlist('estado')
    year = request.args.get('year')
    if not estados or not year:
        return jsonify({'success': False, 'data': None, 'message': 'Parâmetros obrigatórios: estado, year'}), 400
    engine = get_engine()  # Chamada sem o argumento 'context'
    data = fetch_produtividade(engine, estados, year)
    if data:
        return jsonify({'success': True, 'data': data, 'message': 'Dados recuperados com sucesso'})
    else:
        return jsonify({'success': False, 'data': None, 'message': 'Nenhum dado encontrado'}), 404

@bp.route('/quantidade_produzida', methods=['GET'])
def quantidade_produzida():
    municipios = request.args.getlist('municipio')
    anos = request.args.getlist('ano')
    if not municipios or not anos:
        return jsonify({'success': False, 'data': None, 'message': 'Parâmetros obrigatórios: municipio, ano'}), 400
    if len(municipios) * len(anos) > 100:
        return jsonify({'success': False, 'data': None, 'message': 'Número de dados solicitados excede o limite de 100'}), 400
    engine = get_engine()  # Chamada sem o argumento 'context'
    data = fetch_quantidade_produzida(engine, municipios, anos)
    if data:
        return jsonify({'success': True, 'data': data, 'message': 'Dados recuperados com sucesso'})
    else:
        return jsonify({'success': False, 'data': None, 'message': 'Nenhum dado encontrado'}), 404
