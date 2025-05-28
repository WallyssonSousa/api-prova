from flask import Blueprint, jsonify
from models.NotaModel import Nota
from database import db
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from services.GestaoEscolarService import aluno_existe, atividade_existe

nota_bp = Blueprint("nota_bp", __name__)

@nota_bp.route("/notas", methods=["GET"])
@jwt_required()
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

@nota_bp.route("/notas", methods=["POST"])
@jwt_required()
def create_nota():
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem criar salas."}), 403
    
    data = request.get_json()

    required_fields = ["aluno_id", "atividade_id", "nota"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Campo obrigatório ausente: {field}"}), 400

    if not aluno_existe(data["aluno_id"]):
        return jsonify({"error": "Aluno não existe"}), 400

    if not atividade_existe(data["atividade_id"]):
        return jsonify({"error": "Atividade não existe"}), 400

    nota = Nota(
        aluno_id=data["aluno_id"],
        atividade_id=data["atividade_id"],
        nota=data["nota"]
    )

    db.session.add(nota)
    db.session.commit()

    return jsonify({"message": "Nota criada com sucesso"}), 201

@nota_bp.route("/notas/<int:nota_id>", methods=["GET"])
@jwt_required()
def get_nota(nota_id):
    nota = Nota.query.get(nota_id)
    if not nota:
        return jsonify({"error": "Nota não encontrada"}), 404

    return jsonify({
        "id": nota.id,
        "aluno_id": nota.aluno_id,
        "atividade_id": nota.atividade_id,
        "nota": nota.nota
    }), 2007

@nota_bp.route("/notas/<int:nota_id>", methods=["PUT"])
@jwt_required()
def update_nota(nota_id):
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem criar salas."}), 403
    
    nota = Nota.query.get(nota_id)
    if not nota:
        return jsonify({"error": "Nota não encontrada"}), 404

    data = request.get_json()

    if "aluno_id" in data and not aluno_existe(data["aluno_id"]):
        return jsonify({"error": "Aluno não existe"}), 400

    if "atividade_id" in data and not atividade_existe(data["atividade_id"]):
        return jsonify({"error": "Atividade não existe"}), 400

    if "nota" in data:
        nota.nota = data["nota"]

    db.session.commit()

    return jsonify({"message": "Nota atualizada com sucesso"}), 200

@nota_bp.route("/notas/<int:nota_id>", methods=["DELETE"])
@jwt_required()
def delete_nota(nota_id):
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem criar salas."}), 403
    
    nota = Nota.query.get(nota_id)
    if not nota:
        return jsonify({"error": "Nota não encontrada"}), 404

    db.session.delete(nota)
    db.session.commit()

    return jsonify({"message": "Nota deletada com sucesso"}), 200