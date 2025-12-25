# atualizar_banco.py
from app import app, db
from models import Cadastro, Horario
from flask_migrate import Migrate

# Inicializar migrações
migrate = Migrate(app, db)

with app.app_context():
    # Isso criará as migrações
    print("✅ Banco de dados será atualizado...")