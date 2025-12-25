from models.Cadastro import Cadastro
from models.Horario import Horario
from repositories.CadastroRepository import CadastroRepository
from repositories.HorarioRepository import HorarioRepository

class CadastroController:
    
    
    @staticmethod
    def __init__(self):
        self.repository = CadastroRepository()
        
    def criar_cadastro(data):
        # Validações
        if not data.get('nome') or not data.get('email'):
            return False, "Nome e email são obrigatórios"
        
        # Verificar se email já existe
        if data.get('email'):
            existente = CadastroRepository.buscar_por_email(data['email'])
            if existente:
                return False, "Este email já está cadastrado"
        
        # Verificar se documento já existe
        if data.get('documento'):
            existente = CadastroRepository.buscar_por_documento(data['documento'])
            if existente:
                return False, "Este documento já está cadastrado"
        
        try:
            cadastro = CadastroRepository.criar(data)
            return True, "Cadastro criado com sucesso", cadastro
        except Exception as e:
            return False, f"Erro ao criar cadastro: {str(e)}"
    
    @staticmethod
    def listar_cadastros(filtro=None):
        try:
            cadastros = CadastroRepository.listar(filtro)
            total = CadastroRepository.contar_total()
            return True, "Cadastros listados com sucesso", cadastros, total
        except Exception as e:
            return False, f"Erro ao listar cadastros: {str(e)}"
    
    @staticmethod
    def buscar_cadastro(id):
        try:
            cadastro = CadastroRepository.buscar_por_id(id)
            if cadastro:
                # Buscar horários do cadastro
                horarios = HorarioRepository.listar_por_cadastro(id)
                return True, "Cadastro encontrado", cadastro, horarios
            else:
                return False, "Cadastro não encontrado"
        except Exception as e:
            return False, f"Erro ao buscar cadastro: {str(e)}"
    
    @staticmethod
    def atualizar_cadastro(id, data):
        try:
            cadastro = CadastroRepository.buscar_por_id(id)
            if not cadastro:
                return False, "Cadastro não encontrado"
            
            # Verificar se novo email já existe (outro cadastro)
            if data.get('email') and data['email'] != cadastro.email:
                existente = CadastroRepository.buscar_por_email(data['email'])
                if existente:
                    return False, "Este email já está cadastrado em outro cadastro"
            
            # Verificar se novo documento já existe (outro cadastro)
            if data.get('documento') and data['documento'] != cadastro.documento:
                existente = CadastroRepository.buscar_por_documento(data['documento'])
                if existente:
                    return False, "Este documento já está cadastrado em outro cadastro"
            
            cadastro_atualizado = CadastroRepository.atualizar(id, data)
            return True, "Cadastro atualizado com sucesso", cadastro_atualizado
        except Exception as e:
            return False, f"Erro ao atualizar cadastro: {str(e)}"
    
    @staticmethod
    def deletar_cadastro(id):
        try:
            sucesso = CadastroRepository.deletar(id)
            if sucesso:
                return True, "Cadastro deletado com sucesso"
            else:
                return False, "Cadastro não encontrado"
        except Exception as e:
            return False, f"Erro ao deletar cadastro: {str(e)}"