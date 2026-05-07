from flask import Flask
from models import db
from controllers import api_blueprint
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

# O Render usa URLs do Postgres que começam com postgres://, mas o SQLAlchemy exige postgresql://
db_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'minha-chave-secreta-projeto-ifro')

db.init_app(app)
jwt = JWTManager(app)

# Registra as rotas que criamos
app.register_blueprint(api_blueprint)

# Garante que as tabelas sejam criadas no banco de dados ao iniciar
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
