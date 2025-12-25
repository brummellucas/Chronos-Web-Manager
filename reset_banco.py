# reset_banco.py
import os
import sys

print("🔧 RESETANDO BANCO DE DADOS...")

# Remover banco de dados antigo
if os.path.exists('agendamento.db'):
    os.remove('agendamento.db')
    print("✅ Banco de dados antigo removido")

# Remover cache do Python
cache_dirs = ['__pycache__', 'models/__pycache__', 'controllers/__pycache__', 'repositories/__pycache__']
for cache_dir in cache_dirs:
    if os.path.exists(cache_dir):
        import shutil
        shutil.rmtree(cache_dir)
        print(f"✅ Cache removido: {cache_dir}")

print("\n🎉 Agora execute: python app.py")
print("📊 O banco será criado com todas as colunas atualizadas")