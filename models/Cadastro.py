# models/Cadastro.py
from . import db
from datetime import datetime

class Cadastro(db.Model):
    __tablename__ = 'cadastros'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    documento = db.Column(db.String(20), unique=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com horários
    horarios = db.relationship('Horario', backref='cadastro', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, nome, email, telefone=None, documento=None):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.documento = documento
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'documento': self.documento,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M'),
            'total_horarios': len(self.horarios)
        }
    
    def __repr__(self):
        return f'<Cadastro {self.nome}>'