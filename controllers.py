from flask import Blueprint, request, jsonify
from models import db, User, Product
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api_blueprint = Blueprint('api', __name__)

# --- 1. AUTENTICAÇÃO ---
@api_blueprint.route('/registro', methods=['POST'])
def registrar():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"erro": "Usuário já existe"}), 400
    
    # Cria o usuário. Se for passado 'admin' no JSON, ele cria como admin.
    novo_usuario = User(username=data['username'], role=data.get('role', 'usuario'))
    novo_usuario.set_password(data['password'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário criado com sucesso!"}), 201

@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = User.query.filter_by(username=data['username']).first()

    if usuario and usuario.check_password(data['password']):
        # O Token vai guardar quem é o usuário e seu nível de acesso
        token = create_access_token(identity={'id': usuario.id, 'role': usuario.role})
        return jsonify({"token": token}), 200
    return jsonify({"erro": "Credenciais inválidas"}), 401

# --- 2. CRUD DE PRODUTOS ---

# CRIAR (Create)
@api_blueprint.route('/produtos', methods=['POST'])
@jwt_required()
def criar_produto():
    usuario_atual = get_jwt_identity()
    data = request.get_json()
    novo_produto = Product(name=data['name'], owner_id=usuario_atual['id'])
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto criado!"}), 201

# LISTAR (Read)
@api_blueprint.route('/produtos', methods=['GET'])
@jwt_required()
def listar_produtos():
    usuario_atual = get_jwt_identity()
    
    # REGRA DE AUTORIZAÇÃO: Admin vê todos, usuário comum vê apenas os seus
    if usuario_atual['role'] == 'admin':
        produtos = Product.query.all()
    else:
        produtos = Product.query.filter_by(owner_id=usuario_atual['id']).all()
        
    return jsonify([{"id": p.id, "nome": p.name, "dono_id": p.owner_id} for p in produtos])

# EDITAR (Update)
@api_blueprint.route('/produtos/<int:id>', methods=['PUT'])
@jwt_required()
def editar_produto(id):
    usuario_atual = get_jwt_identity()
    produto = Product.query.get(id)

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # REGRA DE AUTORIZAÇÃO: Só o dono ou um admin podem editar
    if usuario_atual['role'] != 'admin' and produto.owner_id != usuario_atual['id']:
        return jsonify({"erro": "Não autorizado"}), 403

    data = request.get_json()
    produto.name = data.get('name', produto.name) # Atualiza o nome
    db.session.commit()
    return jsonify({"mensagem": "Produto atualizado com sucesso!"})

# EXCLUIR (Delete)
@api_blueprint.route('/produtos/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_produto(id):
    usuario_atual = get_jwt_identity()
    produto = Product.query.get(id)

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # REGRA DE AUTORIZAÇÃO: Só o dono ou um admin podem excluir
    if usuario_atual['role'] != 'admin' and produto.owner_id != usuario_atual['id']:
        return jsonify({"erro": "Não autorizado"}), 403

    db.session.delete(produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto deletado com sucesso!"})
