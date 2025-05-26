from database import db

class Atividade(db.Model):
    __tablename__ = 'atividade'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    turma_id = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Date)
    horario_inicio = db.Column(db.Time)
    horario_fim = db.Column(db.Time)

    notas = db.relationship('Nota', backref='atividade', lazy=True)
