from datetime import datetime, date, time
from models.Horario import Horario
from repositories.Database import Database
from sqlalchemy import and_, or_

class HorarioRepository:
    
    @staticmethod
    def criar(horario_data):
        with Database.session_scope() as session:
            # Converter strings para objetos date/time
            data_obj = datetime.strptime(horario_data['data'], '%Y-%m-%d').date()
            hora_inicio_obj = datetime.strptime(horario_data['hora_inicio'], '%H:%M').time()
            hora_fim_obj = datetime.strptime(horario_data['hora_fim'], '%H:%M').time()
            
            horario = Horario(
                cadastro_id=horario_data['cadastro_id'],
                data=data_obj,
                hora_inicio=hora_inicio_obj,
                hora_fim=hora_fim_obj,
                descricao=horario_data.get('descricao')
            )
            session.add(horario)
            session.flush()
            return horario
    
    @staticmethod
    def listar(filtro_data=None, filtro_cadastro=None):
        with Database.session_scope() as session:
            query = session.query(Horario).join(Horario.cadastro)
            
            if filtro_data:
                data_obj = datetime.strptime(filtro_data, '%Y-%m-%d').date()
                query = query.filter(Horario.data == data_obj)
            
            if filtro_cadastro:
                query = query.filter(Horario.cadastro_id == filtro_cadastro)
            
            return query.order_by(Horario.data, Horario.hora_inicio).all()
    
    @staticmethod
    def buscar_por_id(id):
        with Database.session_scope() as session:
            return session.query(Horario).get(id)
    
    @staticmethod
    def listar_por_cadastro(cadastro_id):
        with Database.session_scope() as session:
            return session.query(Horario)\
                .filter_by(cadastro_id=cadastro_id)\
                .order_by(Horario.data, Horario.hora_inicio)\
                .all()
    
    @staticmethod
    def verificar_disponibilidade(data, hora_inicio, hora_fim, horario_id=None):
        with Database.session_scope() as session:
            # Converter para objetos
            data_obj = datetime.strptime(data, '%Y-%m-%d').date()
            inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()
            fim_obj = datetime.strptime(hora_fim, '%H:%M').time()
            
            query = session.query(Horario).filter(
                and_(
                    Horario.data == data_obj,
                    or_(
                        and_(Horario.hora_inicio < fim_obj, Horario.hora_fim > inicio_obj),
                        and_(Horario.hora_inicio >= inicio_obj, Horario.hora_fim <= fim_obj)
                    )
                )
            )
            
            if horario_id:
                query = query.filter(Horario.id != horario_id)
            
            return query.count() == 0
    
    @staticmethod
    def atualizar(id, horario_data):
        with Database.session_scope() as session:
            horario = session.query(Horario).get(id)
            if horario:
                if 'data' in horario_data:
                    horario.data = datetime.strptime(horario_data['data'], '%Y-%m-%d').date()
                if 'hora_inicio' in horario_data:
                    horario.hora_inicio = datetime.strptime(horario_data['hora_inicio'], '%H:%M').time()
                if 'hora_fim' in horario_data:
                    horario.hora_fim = datetime.strptime(horario_data['hora_fim'], '%H:%M').time()
                if 'cadastro_id' in horario_data:
                    horario.cadastro_id = horario_data['cadastro_id']
                if 'descricao' in horario_data:
                    horario.descricao = horario_data['descricao']
            return horario
    
    @staticmethod
    def deletar(id):
        with Database.session_scope() as session:
            horario = session.query(Horario).get(id)
            if horario:
                session.delete(horario)
                return True
            return False
    
    @staticmethod
    def contar_total():
        with Database.session_scope() as session:
            return session.query(Horario).count()
    
    @staticmethod
    def listar_por_periodo(data_inicio, data_fim):
        with Database.session_scope() as session:
            inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            
            return session.query(Horario)\
                .filter(and_(Horario.data >= inicio_obj, Horario.data <= fim_obj))\
                .order_by(Horario.data, Horario.hora_inicio)\
                .all()