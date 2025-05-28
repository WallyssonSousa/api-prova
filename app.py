import os
from flask import Flask, jsonify
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from database import db
from models.UserModel import User
from routes.AuthRoute import auth_bp
from routes.HomeRoute import home_bp
from routes.AtividadeRoute import atividade_bp
from routes.NotaRoute import nota_bp
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(atividade_bp)
app.register_blueprint(nota_bp)

with app.app_context():
    db.create_all()

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        print("Variáveis ADMIN_USERNAME e ADMIN_PASSWORD devem estar definidas para criação do 1º usuário root.")
        exit(1)

    if User.query.filter_by(username=admin_username).first():
        print(f"Usuário admin: '{admin_username}'")
    else:
        hashed_password = generate_password_hash(admin_password)
        admin = User(username=admin_username, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Usuário admin '{admin_username}' criado com sucesso.")

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bem-vindo à API de adicionar prova"})

if __name__ == '__main__':
    app.run(port=app.config.get("PORT", 5001), debug=True)