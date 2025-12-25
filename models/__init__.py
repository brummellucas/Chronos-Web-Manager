# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Crie uma ÚNICA instância do SQLAlchemy aqui
db = SQLAlchemy()

# Importe os modelos
from .Cadastro import Cadastro
from .Horario import Horario

__all__ = ['db', 'Cadastro', 'Horario']