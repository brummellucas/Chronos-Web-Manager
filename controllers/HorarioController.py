from datetime import datetime
from repositories.HorarioRepository import HorarioRepository
from repositories.CadastroRepository import CadastroRepository

class HorarioController:
    
    @staticmethod
    def criar_horario(data):
        # Validações
        required_fields = ['cadastro_id', 'data', 'hora_inicio', 'hora_fim']
        for field in required_fields:
            if not data.get(field):
                return False, f"Campo {field.replace('_', ' ')} é obrigatório"
        
        # Verificar se cadastro existe
        cadastro = CadastroRepository.buscar_por_id(data['cadastro_id'])
        if not cadastro:
            return False, "Cadastro não encontrado"
        
        # Validar horários
        if not HorarioController._validar_horario(data['hora_inicio'], data['hora_fim']):
            return False, "Horário inválido. Hora de início deve ser anterior à hora de fim"
        
        # Verificar disponibilidade
        if not HorarioRepository.verificar_disponibilidade(
            data['data'], data['hora_inicio'], data['hora_fim']
        ):
            return False, "Já existe um horário agendado para este período"
        
        try:
            horario = HorarioRepository.criar(data)
            return True, "Horário criado com sucesso", horario
        except Exception as e:
            return False, f"Erro ao criar horário: {str(e)}"
    
    @staticmethod
    def listar_horarios(filtro_data=None, filtro_cadastro=None):
        try:
            horarios = HorarioRepository.listar(filtro_data, filtro_cadastro)
            total = HorarioRepository.contar_total()
            cadastros = CadastroRepository.listar()
            return True, "Horários listados com sucesso", horarios, total, cadastros
        except Exception as e:
            return False, f"Erro ao listar horários: {str(e)}"
    
    @staticmethod
    def buscar_horario(id):
        try:
            horario = HorarioRepository.buscar_por_id(id)
            if horario:
                return True, "Horário encontrado", horario
            else:
                return False, "Horário não encontrado"
        except Exception as e:
            return False, f"Erro ao buscar horário: {str(e)}"
    
    @staticmethod
    def listar_horarios_por_cadastro(cadastro_id):
        try:
            # Verificar se cadastro existe
            cadastro = CadastroRepository.buscar_por_id(cadastro_id)
            if not cadastro:
                return False, "Cadastro não encontrado"
            
            horarios = HorarioRepository.listar_por_cadastro(cadastro_id)
            return True, f"Horários do cadastro", horarios, cadastro
        except Exception as e:
            return False, f"Erro ao listar horários: {str(e)}"
    
    @staticmethod
    def atualizar_horario(id, data):
        try:
            horario = HorarioRepository.buscar_por_id(id)
            if not horario:
                return False, "Horário não encontrado"
            
            # Se mudar o cadastro, verificar se existe
            if 'cadastro_id' in data:
                cadastro = CadastroRepository.buscar_por_id(data['cadastro_id'])
                if not cadastro:
                    return False, "Novo cadastro não encontrado"
            
            # Validar horários se fornecidos
            if 'hora_inicio' in data and 'hora_fim' in data:
                if not HorarioController._validar_horario(data['hora_inicio'], data['hora_fim']):
                    return False, "Horário inválido"
            
            # Usar valores atuais se não fornecidos
            data_verificacao = data.get('data') or horario.data.strftime('%Y-%m-%d')
            hora_inicio_verificacao = data.get('hora_inicio') or horario.hora_inicio.strftime('%H:%M')
            hora_fim_verificacao = data.get('hora_fim') or horario.hora_fim.strftime('%H:%M')
            
            # Verificar disponibilidade (exceto o próprio horário)
            if not HorarioRepository.verificar_disponibilidade(
                data_verificacao, hora_inicio_verificacao, hora_fim_verificacao, id
            ):
                return False, "Já existe um horário agendado para este período"
            
            horario_atualizado = HorarioRepository.atualizar(id, data)
            return True, "Horário atualizado com sucesso", horario_atualizado
        except Exception as e:
            return False, f"Erro ao atualizar horário: {str(e)}"
    
    @staticmethod
    def deletar_horario(id):
        try:
            sucesso = HorarioRepository.deletar(id)
            if sucesso:
                return True, "Horário deletado com sucesso"
            else:
                return False, "Horário não encontrado"
        except Exception as e:
            return False, f"Erro ao deletar horário: {str(e)}"
    
    @staticmethod
    def relatorio_periodo(data_inicio, data_fim):
        try:
            horarios = HorarioRepository.listar_por_periodo(data_inicio, data_fim)
            return True, "Relatório gerado com sucesso", horarios
        except Exception as e:
            return False, f"Erro ao gerar relatório: {str(e)}"
    
    @staticmethod
    def _validar_horario(hora_inicio, hora_fim):
        """Valida se hora_inicio é anterior a hora_fim"""
        try:
            inicio = datetime.strptime(hora_inicio, '%H:%M')
            fim = datetime.strptime(hora_fim, '%H:%M')
            return inicio < fim
        except ValueError:
            return False