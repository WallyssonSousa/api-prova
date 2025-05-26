from models.AtividadeModel import Atividade
import requests

BASE_URL = "https://gestao-escolar-api-3uu5.onrender.com/"
TOKEN_CACHE = {"token": None}

ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "e4340d5ce26ec43f2274105cc4a6dd67"
}

def get_token():
    if TOKEN_CACHE["token"]:
        return TOKEN_CACHE["token"]

    res = requests.post(f"{BASE_URL}/login", json=ADMIN_CREDENTIALS)

    if res.status_code == 200:
        token = res.json().get("access_token")
        TOKEN_CACHE["token"] = token
        return token

    return None

def get_headers():
    token = get_token()
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}

def professor_existe(professor_id):
    headers = get_headers()
    if not headers:
        return False
    res = requests.get(f"{BASE_URL}/professores/{professor_id}", headers=headers)
    return res.status_code == 200

def turma_existe(turma_id):
    headers = get_headers()
    if not headers:
        return False
    res = requests.get(f"{BASE_URL}/turmas/{turma_id}", headers=headers)
    return res.status_code == 200


def aluno_existe(aluno_id):
    headers = get_headers()
    if not headers:
        return False
    res = requests.get(f"{BASE_URL}/alunos/{aluno_id}", headers=headers)
    return res.status_code == 200


def get_alunos_da_turma(turma_id):
    headers = get_headers()
    if not headers:
        return []

    res = requests.get(f"{BASE_URL}/turmas/{turma_id}/alunos", headers=headers)
    if res.status_code == 200:
        return res.json()  
    return []


def atividade_existe(atividade_id):
    return Atividade.query.get(atividade_id) is not None


def get_turma_nome(turma_id):
    headers = get_headers()
    if not headers:
        return None

    res = requests.get(f"{BASE_URL}/turmas/{turma_id}", headers=headers)
    if res.status_code == 200:
        return res.json().get("nome")
    return None


