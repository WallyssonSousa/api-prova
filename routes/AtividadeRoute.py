from flask import Blueprint, jsonify
from models.AtividadeModel import Atividade

atividade_bp = Blueprint("atividade_bp", __name__)

@atividade_bp.route("/atividades", methods=["GET"])
def get_atividades():
    atividades = Atividade.query.all()
    resultado = []

    for atividade in atividades:
        resultado.append({
            "id": atividade.id,
            "titulo": atividade.titulo,
            "descricao": atividade.descricao,
            "turma_id": atividade.turma_id,
            "data": atividade.data.strftime("%Y-%m-%d") if atividade.data else None
        })

    return jsonify(resultado), 200
