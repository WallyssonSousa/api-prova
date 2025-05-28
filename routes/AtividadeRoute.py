from flask import Blueprint, jsonify
from models.AtividadeModel import Atividade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from database import db
from services.GestaoEscolarService import get_turma_nome, turma_existe
from datetime import datetime

atividade_bp = Blueprint("atividade_bp", __name__)

@atividade_bp.route("/atividades", methods=["GET"])
@jwt_required()
def get_atividades():
    atividades = Atividade.query.all()
    resultado = []

    for atividade in atividades:
        resultado.append({
            "id": atividade.id,
            "titulo": atividade.titulo,
            "descricao": atividade.descricao,
            "turma_id": atividade.turma_id,
            "turma_nome": get_turma_nome(atividade.turma_id),
            "data": atividade.data.strftime("%Y-%m-%d") if atividade.data else None,
            "horario_inicio": atividade.horario_inicio.strftime("%H:%M") if atividade.horario_inicio else None,
            "horario_fim": atividade.horario_fim.strftime("%H:%M") if atividade.horario_fim else None,
            "notas": [
                {
                    "id": nota.id,
                    "aluno_id": nota.aluno_id,
                    "nota": nota.nota
                } for nota in atividade.notas
            ]
        })

    return jsonify(resultado), 200

@atividade_bp.route("/atividades/<int:atividade_id>", methods=["GET"])
@jwt_required()
def get_atividade(atividade_id):
    atividade = Atividade.query.get(atividade_id)
    if not atividade:
        return jsonify({"error": "Atividade não encontrada"}), 404

    resultado = {
        "id": atividade.id,
        "titulo": atividade.titulo,
        "descricao": atividade.descricao,
        "turma_id": atividade.turma_id,
        "turma_nome": get_turma_nome(atividade.turma_id),
        "data": atividade.data.strftime("%Y-%m-%d") if atividade.data else None,
        "horario_inicio": atividade.horario_inicio.strftime("%H:%M") if atividade.horario_inicio else None,
        "horario_fim": atividade.horario_fim.strftime("%H:%M") if atividade.horario_fim else None,
        "notas": [
            {
                "id": nota.id,
                "aluno_id": nota.aluno_id,
                "nota": nota.nota
            } for nota in atividade.notas
        ]
    }

    return jsonify(resultado), 200

@atividade_bp.route("/atividades", methods=["POST"])
@jwt_required()
def create_atividade():
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem criar salas."}), 403
    
    data = request.get_json()

    if not turma_existe(data["turma_id"]):
        return jsonify({"error": "Turma não existe"}), 400
    
    required_fields = ["titulo", "descricao", "turma_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo obrigatório ausente: {field}"}), 400

    
    atividade = Atividade(
        titulo=data["titulo"], 
        descricao=data["descricao"],
        turma_id=data["turma_id"],
        data=datetime.strptime(data["data"], "%Y-%m-%d").date() if data.get("data") else None,
        horario_inicio=datetime.strptime(data["horario_inicio"], "%H:%M").time() if data.get("horario_inicio") else None,
        horario_fim=datetime.strptime(data["horario_fim"], "%H:%M").time() if data.get("horario_fim") else None
    )

    db.session.add(atividade)
    db.session.commit()

    return jsonify({"message": "Atividade criada com sucesso", "atividade_id": atividade.id}), 201


@atividade_bp.route("/atividades/<int:atividade_id>", methods=["PUT"])
@jwt_required()
def update_atividade(atividade_id):
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem criar salas."}), 403
    
    data = request.get_json() 
    atividade = Atividade.query.get(atividade_id)

    if not atividade:
        return jsonify({"error": "Atividade não encontrada"}), 404
    if data.get("turma_id") and not turma_existe(data["turma_id"]):
        return jsonify({"error": "Turma não existe"}), 400
    
    atividade.titulo = data.get("titulo", atividade.titulo)
    atividade.descricao = data.get("descricao", atividade.descricao)
    atividade.turma_id = data.get("turma_id", atividade.turma_id)
    if "data" in data:
        atividade.data = datetime.strptime(data["data"], "%Y-%m-%d").date()

    if "horario_inicio" in data:
        atividade.horario_inicio = datetime.strptime(data["horario_inicio"], "%H:%M").time()

    if "horario_fim" in data:
        atividade.horario_fim = datetime.strptime(data["horario_fim"], "%H:%M").time()


    db.session.commit()

    return jsonify({"message": "Atividade atualizada com sucesso"}), 200

@atividade_bp.route("/atividades/<int:atividade_id>", methods=["DELETE"])
@jwt_required()
def delete_atividade(atividade_id):
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem criar salas."}), 403
    
    atividade = Atividade.query.get(atividade_id)

    if not atividade:
        return jsonify({"error": "Atividade não encontrada"}), 404

    db.session.delete(atividade)
    db.session.commit()

    return jsonify({"message": "Atividade deletada com sucesso"}), 200

