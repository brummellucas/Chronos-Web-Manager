from models.Cadastro import Cadastro
from repositories.Database import Database
from sqlalchemy import or_

class CadastroRepository:
    
    @staticmethod
    def criar(cadastro_data):
        with Database.session_scope() as session:
            cadastro = Cadastro(
                nome=cadastro_data['nome'],
                email=cadastro_data['email'],
                telefone=cadastro_data.get('telefone'),
                documento=cadastro_data.get('documento')
            )
            session.add(cadastro)
            session.flush()
            return cadastro
    
    @staticmethod
    def listar(filtro=None):
        with Database.session_scope() as session:
            query = session.query(Cadastro)
            if filtro:
                query = query.filter(
                    or_(
                        Cadastro.nome.ilike(f'%{filtro}%'),
                        Cadastro.email.ilike(f'%{filtro}%'),
                        Cadastro.documento.ilike(f'%{filtro}%')
                    )
                )
            return query.order_by(Cadastro.nome).all()
    
    @staticmethod
    def buscar_por_id(id):
        with Database.session_scope() as session:
            return session.query(Cadastro).get(id)
    
    @staticmethod
    def buscar_por_documento(documento):
        with Database.session_scope() as session:
            return session.query(Cadastro).filter_by(documento=documento).first()
    
    @staticmethod
    def buscar_por_email(email):
        with Database.session_scope() as session:
            return session.query(Cadastro).filter_by(email=email).first()
    
    @staticmethod
    def atualizar(id, cadastro_data):
        with Database.session_scope() as session:
            cadastro = session.query(Cadastro).get(id)
            if cadastro:
                cadastro.nome = cadastro_data['nome']
                cadastro.email = cadastro_data['email']
                cadastro.telefone = cadastro_data.get('telefone')
                cadastro.documento = cadastro_data.get('documento')
            return cadastro
    
    @staticmethod
    def deletar(id):
        with Database.session_scope() as session:
            cadastro = session.query(Cadastro).get(id)
            if cadastro:
                session.delete(cadastro)
                return True
            return False
    
    @staticmethod
    def contar_total():
        with Database.session_scope() as session:
            return session.query(Cadastro).count()