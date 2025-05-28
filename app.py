from flask import Flask, jsonify
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from database import db
from routes.HomeRoute import home_bp
from routes.AtividadeRoute import atividade_bp
from routes.NotaRoute import nota_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(atividade_bp)
app.register_blueprint(nota_bp)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bem-vindo à API de adicionar prova"})

if __name__ == '__main__':
    app.run(port=app.config.get("PORT", 5001), debug=True)