# models/Horario.py
from . import db
from datetime import datetime, time, date as date_type

class Horario(db.Model):
    __tablename__ = 'horarios'
    
    id = db.Column(db.Integer, primary_key=True)
    cadastro_id = db.Column(db.Integer, db.ForeignKey('cadastros.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20), default='agendado')
    tipo_servico = db.Column(db.String(50))
    prioridade = db.Column(db.String(20), default='normal')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __init__(self, cadastro_id, data, hora_inicio, hora_fim, descricao=None, 
                 status='agendado', tipo_servico=None, prioridade='normal'):
        self.cadastro_id = cadastro_id
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.descricao = descricao
        self.status = status
        self.tipo_servico = tipo_servico
        self.prioridade = prioridade
    
    def to_dict(self):
        return {
            'id': self.id,
            'cadastro_id': self.cadastro_id,
            'cadastro_nome': self.cadastro.nome if self.cadastro else 'N/A',
            'data': self.data.strftime('%d/%m/%Y'),
            'hora_inicio': self.hora_inicio.strftime('%H:%M'),
            'hora_fim': self.hora_fim.strftime('%H:%M'),
            'descricao': self.descricao,
            'status': self.status,
            'tipo_servico': self.tipo_servico,
            'prioridade': self.prioridade,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M') if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.strftime('%d/%m/%Y %H:%M') if self.data_atualizacao else None,
            'duracao': self.calcular_duracao()
        }
    
    def calcular_duracao(self):
        inicio = datetime.combine(datetime.today(), self.hora_inicio)
        fim = datetime.combine(datetime.today(), self.hora_fim)
        duracao = fim - inicio
        horas = duracao.seconds // 3600
        minutos = (duracao.seconds % 3600) // 60
        return f"{horas}h {minutos}min"
    
    def __repr__(self):
        return f'<Horario {self.data} {self.hora_inicio}-{self.hora_fim}>'