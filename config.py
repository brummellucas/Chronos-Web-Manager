import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-aqui-12345-mude-isso-em-producao'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///agendamento.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Mude para True para ver queries SQL no terminal