from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from database import db
from routes.AtividadeRoute import atividade_bp
from routes.NotaRoute import nota_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

app.register_blueprint(atividade_bp)
app.register_blueprint(nota_bp)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Flask app!"

if __name__ == '__main__':
    app.run(port=5002, debug=True)