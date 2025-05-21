from flask import Blueprint, jsonify
from models.NotaModel import Nota

nota_bp = Blueprint("nota_bp", __name__)

@nota_bp.route("/notas", methods=["GET"])
def get_notas():
    notas = Nota.query.all()
    resultado = []

    for nota in notas:
        resultado.append({
            "id": nota.id,
            "aluno_id": nota.aluno_id,
            "atividade_id": nota.atividade_id,
            "nota": nota.nota
        })

    return jsonify(resultado), 200
