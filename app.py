# app.py - VERSÃO COMPLETA COM EXPORTAÇÃO CSV
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response
from config import Config
from datetime import datetime, date, timedelta
import csv
import io

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Importar db dos models
    from models import db
    db.init_app(app)
    
    # Importar modelos
    from models import Cadastro, Horario
    
    # Inicializar banco de dados
    with app.app_context():
        db.create_all()
        
        # Adicionar alguns dados de exemplo se o banco estiver vazio
        if Cadastro.query.count() == 0:
            cadastros_exemplo = [
                Cadastro(nome='João Silva', email='joao@email.com', telefone='(11) 99999-9999', documento='123.456.789-00'),
                Cadastro(nome='Maria Santos', email='maria@email.com', telefone='(11) 98888-8888', documento='987.654.321-00'),
                Cadastro(nome='Pedro Oliveira', email='pedro@email.com', telefone='(11) 97777-7777'),
                Cadastro(nome='Ana Costa', email='ana@email.com', telefone='(11) 96666-6666', documento='456.789.123-00'),
                Cadastro(nome='Carlos Pereira', email='carlos@email.com', telefone='(11) 95555-5555')
            ]
            
            for cadastro in cadastros_exemplo:
                db.session.add(cadastro)
            
            db.session.commit()
            print("✅ Dados de exemplo criados!")
    
    # Configurar secret key para flash messages
    app.secret_key = app.config['SECRET_KEY']
    
    # ========== ROTAS ==========
    
    @app.route('/')
    def index():
        with app.app_context():
            total_cadastros = Cadastro.query.count()
            total_horarios = Horario.query.count()
            
            hoje = date.today()
            horarios_hoje = Horario.query.filter_by(data=hoje).count()
            
            # Próximos horários (próximos 7 dias)
            semana_fim = hoje + timedelta(days=7)
            proximos_horarios = Horario.query.filter(
                Horario.data >= hoje,
                Horario.data <= semana_fim
            ).order_by(Horario.data, Horario.hora_inicio).limit(5).all()
            
            # Últimos cadastros
            ultimos_cadastros = Cadastro.query.order_by(Cadastro.data_criacao.desc()).limit(5).all()
            
            # Eventos para o calendário (próximos 30 dias)
            mes_fim = hoje + timedelta(days=30)
            eventos_calendario = Horario.query.filter(
                Horario.data >= hoje,
                Horario.data <= mes_fim
            ).all()
            
            # Calcular disponibilidade
            horarios_mes = Horario.query.filter(
                Horario.data >= hoje.replace(day=1),
                Horario.data <= (hoje.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            ).count()
            
            # Supondo 8 horas úteis por dia, 22 dias úteis no mês = 176 horas
            horas_totais = 176 * 60  # em minutos
            horas_ocupadas = sum([
                (h.hora_fim.hour * 60 + h.hora_fim.minute) - 
                (h.hora_inicio.hour * 60 + h.hora_inicio.minute)
                for h in Horario.query.filter(
                    Horario.data >= hoje.replace(day=1),
                    Horario.data <= (hoje.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                ).all()
            ])
            
            disponibilidade = max(0, 100 - int((horas_ocupadas / horas_totais) * 100)) if horas_totais > 0 else 100
            vagas_restantes = max(0, (horas_totais - horas_ocupadas) // 60)
            
            # Semana atual para o calendário semanal
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            dias_semana = []
            for i in range(7):
                dia_data = inicio_semana + timedelta(days=i)
                eventos_dia = [h for h in eventos_calendario if h.data == dia_data]
                dias_semana.append({
                    'data': dia_data,
                    'eventos': [{
                        'hora': f"{h.hora_inicio.strftime('%H:%M')}-{h.hora_fim.strftime('%H:%M')}",
                        'cliente': h.cadastro.nome[:10] + '...' if len(h.cadastro.nome) > 10 else h.cadastro.nome,
                        'cor': '#4361ee'
                    } for h in eventos_dia[:2]]  # Limitar a 2 eventos por dia para visualização
                })
            
            semana_atual = f"{inicio_semana.strftime('%d/%m')} - {(inicio_semana + timedelta(days=6)).strftime('%d/%m')}"
            
            return render_template('index.html',
                                 total_cadastros=total_cadastros,
                                 total_horarios=total_horarios,
                                 horarios_hoje=horarios_hoje,
                                 hoje=hoje.strftime('%Y-%m-%d'),
                                 data_hoje=hoje.strftime('%d/%m/%Y'),
                                 disponibilidade=disponibilidade,
                                 vagas_restantes=vagas_restantes,
                                 proximos_horarios=proximos_horarios,
                                 ultimos_cadastros=ultimos_cadastros,
                                 eventos_calendario=eventos_calendario,
                                 semana_atual=semana_atual,
                                 semana=dias_semana)
    
    @app.route('/cadastros')
    def listar_cadastros():
        with app.app_context():
            filtro = request.args.get('filtro', '')
            
            if filtro:
                cadastros = Cadastro.query.filter(
                    (Cadastro.nome.ilike(f'%{filtro}%')) |
                    (Cadastro.email.ilike(f'%{filtro}%')) |
                    (Cadastro.documento.ilike(f'%{filtro}%'))
                ).order_by(Cadastro.nome).all()
            else:
                cadastros = Cadastro.query.order_by(Cadastro.nome).all()
            
            total = len(cadastros)
            
            # Criar versão "limpa" dos nomes sem aspas simples
            for cadastro in cadastros:
                # Remove aspas simples e duplas para segurança no JavaScript
                cadastro.nome_limpo = cadastro.nome.replace("'", "").replace('"', '')
                # Opcional: também limpar o email se for usar em JavaScript
                cadastro.email_limpo = cadastro.email.replace("'", "").replace('"', '') if cadastro.email else ''
            
            return render_template('cadastros/listar.html', 
                                 cadastros=cadastros, 
                                 total=total,
                                 filtro=filtro)
    
    @app.route('/cadastros/novo', methods=['GET', 'POST'])
    def criar_cadastro():
        if request.method == 'POST':
            try:
                with app.app_context():
                    # Verificar se email já existe
                    email_existente = Cadastro.query.filter_by(email=request.form['email']).first()
                    if email_existente:
                        flash('Este email já está cadastrado!', 'error')
                        return render_template('cadastros/criar.html', form_data=request.form)
                    
                    # Verificar se documento já existe
                    documento = request.form.get('documento')
                    if documento:
                        documento_existente = Cadastro.query.filter_by(documento=documento).first()
                        if documento_existente:
                            flash('Este documento já está cadastrado!', 'error')
                            return render_template('cadastros/criar.html', form_data=request.form)
                    
                    cadastro = Cadastro(
                        nome=request.form['nome'],
                        email=request.form['email'],
                        telefone=request.form.get('telefone'),
                        documento=documento
                    )
                    
                    db.session.add(cadastro)
                    db.session.commit()
                    
                    flash('Cadastro criado com sucesso!', 'success')
                    return redirect(url_for('listar_cadastros'))
                    
            except Exception as e:
                flash(f'Erro ao criar cadastro: {str(e)}', 'error')
                return render_template('cadastros/criar.html', form_data=request.form)
        
        return render_template('cadastros/criar.html')
    
    @app.route('/cadastros/<int:id>')
    def visualizar_cadastro(id):
        with app.app_context():
            cadastro = Cadastro.query.get_or_404(id)
            horarios = Horario.query.filter_by(cadastro_id=id).order_by(Horario.data.desc(), Horario.hora_inicio).all()
            
            hoje = date.today()
            horarios_confirmados = len([h for h in horarios if h.status == 'confirmado'])
            horarios_pendentes = len([h for h in horarios if h.status == 'pendente'])
            
            # Atividades simuladas
            atividades = [
                {'titulo': 'Cadastro criado', 'descricao': 'Cadastro realizado no sistema', 'data': cadastro.data_criacao},
                {'titulo': 'Primeiro agendamento', 'descricao': 'Primeiro horário agendado', 'data': datetime.now() - timedelta(days=5)} if horarios else None,
                {'titulo': 'Atualização de dados', 'descricao': 'Informações atualizadas', 'data': datetime.now() - timedelta(days=2)} if cadastro.data_criacao < datetime.now() - timedelta(days=2) else None
            ]
            atividades = [a for a in atividades if a is not None]
            
            return render_template('cadastros/visualizar.html', 
                                 cadastro=cadastro, 
                                 horarios=horarios,
                                 hoje=hoje,
                                 horarios_confirmados=horarios_confirmados,
                                 horarios_pendentes=horarios_pendentes,
                                 atividades=atividades)
    
    @app.route('/cadastros/<int:id>/editar', methods=['GET', 'POST'])
    def editar_cadastro(id):
        with app.app_context():
            cadastro = Cadastro.query.get_or_404(id)
            
            if request.method == 'POST':
                try:
                    # Verificar se novo email já existe (outro cadastro)
                    novo_email = request.form['email']
                    if novo_email != cadastro.email:
                        email_existente = Cadastro.query.filter(
                            Cadastro.email == novo_email,
                            Cadastro.id != id
                        ).first()
                        if email_existente:
                            flash('Este email já está cadastrado em outro cadastro!', 'error')
                            return render_template('cadastros/editar.html', cadastro=cadastro, form_data=request.form)
                    
                    # Verificar se novo documento já existe (outro cadastro)
                    novo_documento = request.form.get('documento')
                    if novo_documento and novo_documento != cadastro.documento:
                        documento_existente = Cadastro.query.filter(
                            Cadastro.documento == novo_documento,
                            Cadastro.id != id
                        ).first()
                        if documento_existente:
                            flash('Este documento já está cadastrado em outro cadastro!', 'error')
                            return render_template('cadastros/editar.html', cadastro=cadastro, form_data=request.form)
                    
                    cadastro.nome = request.form['nome']
                    cadastro.email = novo_email
                    cadastro.telefone = request.form.get('telefone')
                    cadastro.documento = novo_documento
                    
                    db.session.commit()
                    
                    flash('Cadastro atualizado com sucesso!', 'success')
                    return redirect(url_for('visualizar_cadastro', id=id))
                    
                except Exception as e:
                    flash(f'Erro ao atualizar cadastro: {str(e)}', 'error')
                    return render_template('cadastros/editar.html', cadastro=cadastro, form_data=request.form)
            
            return render_template('cadastros/editar.html', cadastro=cadastro)
    
    @app.route('/cadastros/<int:id>/deletar', methods=['POST'])
    def deletar_cadastro(id):
        print(f"🔍 DEBUG: Iniciando exclusão do cadastro ID: {id}")
        try:
            with app.app_context():
                # Buscar o cadastro
                cadastro = Cadastro.query.get_or_404(id)
                
                print(f"📋 DEBUG: Cadastro encontrado - {cadastro.nome}")
                print(f"📋 DEBUG: Horários associados: {len(cadastro.horarios)}")
                
                # 🔍 Opcional: Verificar se tem horários futuros
                hoje = date.today()
                
                horarios_futuros = Horario.query.filter(
                    Horario.cadastro_id == id,
                    Horario.data >= hoje
                ).all()
                
                if horarios_futuros:
                    flash(f'⚠️ Não é possível excluir! Existem {len(horarios_futuros)} horário(s) futuro(s) agendado(s).', 'warning')
                    return redirect(url_for('visualizar_cadastro', id=id))
                
                # 🔧 Excluir o cadastro (os horários serão excluídos em cascata)
                db.session.delete(cadastro)
                db.session.commit()
                
                print(f"✅ DEBUG: Cadastro {id} excluído com sucesso!")
                flash('✅ Cadastro excluído com sucesso!', 'success')
                return redirect(url_for('listar_cadastros'))
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ DEBUG: Erro ao excluir: {str(e)}")
            flash(f'❌ Erro ao excluir cadastro: {str(e)}', 'danger')
            return redirect(url_for('listar_cadastros'))
    
    @app.route('/horarios')
    def listar_horarios():
        with app.app_context():
            filtro_data = request.args.get('data', '')
            filtro_cadastro = request.args.get('cadastro', '')
        
        query = Horario.query
        
        if filtro_data:
            try:
                data_filtro = datetime.strptime(filtro_data, '%Y-%m-%d').date()
                query = query.filter_by(data=data_filtro)
            except ValueError:
                pass
        
        if filtro_cadastro:
            try:
                cadastro_id = int(filtro_cadastro)
                query = query.filter_by(cadastro_id=cadastro_id)
            except ValueError:
                pass
        
        horarios = query.order_by(Horario.data, Horario.hora_inicio).all()
        total = len(horarios)
        cadastros = Cadastro.query.order_by(Cadastro.nome).all()
        
        hoje = date.today()
        hoje_count = Horario.query.filter_by(data=hoje).count()
        
        # 🔧 CALCULAR DATAS PARA O MODAL
        data_fim_padrao = (hoje + timedelta(days=30)).strftime('%Y-%m-%d')
        hoje_str = hoje.strftime('%Y-%m-%d')
        
        # Preparar dados para o template
        for horario in horarios:
            # Nome limpo do cliente (sem aspas)
            horario.nome_cliente_limpo = horario.cadastro.nome.replace("'", "").replace('"', '')
            # Data formatada
            horario.data_formatada = horario.data.strftime('%d/%m/%Y')
            # Horários formatados
            horario.hora_inicio_str = horario.hora_inicio.strftime('%H:%M')
            horario.hora_fim_str = horario.hora_fim.strftime('%H:%M')
            # Descrição limpa (se existir)
            if horario.descricao:
                horario.descricao_limpa = horario.descricao.replace("'", "").replace('"', '')[:30]
            else:
                horario.descricao_limpa = ''
        
        # Semana atual para visualização
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        dias_semana = []
        for i in range(7):
            dia_data = inicio_semana + timedelta(days=i)
            eventos_dia = [h for h in horarios if h.data == dia_data]
            dias_semana.append({
                'data': dia_data,
                'eventos': [{
                    'hora': f"{h.hora_inicio_str}-{h.hora_fim_str}",
                    'cliente': h.cadastro.nome[:10] + '...' if len(h.cadastro.nome) > 10 else h.cadastro.nome,
                    'cor': '#4361ee',
                    'id': h.id
                } for h in eventos_dia[:2]]
            })
        
        semana_atual = f"{inicio_semana.strftime('%d/%m')} - {(inicio_semana + timedelta(days=6)).strftime('%d/%m')}"
        
        return render_template('horarios/listar.html',
                             horarios=horarios,
                             total=total,
                             cadastros=cadastros,
                             filtro_data=filtro_data,
                             filtro_cadastro=filtro_cadastro,
                             hoje=hoje,
                             hoje_str=hoje_str,           # ← NOVO
                             data_fim_padrao=data_fim_padrao, # ← NOVO
                             hoje_count=hoje_count,
                             semana_atual=semana_atual,
                             semana=dias_semana,  timedelta=timedelta)
    
    @app.route('/horarios/novo', methods=['GET', 'POST'])
    def criar_horario():
        with app.app_context():
            cadastros = Cadastro.query.order_by(Cadastro.nome).all()
            
            if request.method == 'POST':
                try:
                    # Validar dados
                    cadastro_id = int(request.form['cadastro_id'])
                    data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
                    hora_inicio = datetime.strptime(request.form['hora_inicio'], '%H:%M').time()
                    hora_fim = datetime.strptime(request.form['hora_fim'], '%H:%M').time()
                    
                    # Verificar se data não é no passado
                    if data < date.today():
                        flash('Não é possível agendar para datas passadas!', 'error')
                        return render_template('horarios/criar.html', cadastros=cadastros, form_data=request.form)
                    
                    # Verificar se hora fim é maior que hora início
                    if hora_fim <= hora_inicio:
                        flash('A hora de término deve ser posterior à hora de início!', 'error')
                        return render_template('horarios/criar.html', cadastros=cadastros, form_data=request.form)
                    
                    # Verificar se já existe horário no mesmo período
                    conflito = Horario.query.filter(
                        Horario.data == data,
                        Horario.cadastro_id == cadastro_id,
                        ((Horario.hora_inicio < hora_fim) & (Horario.hora_fim > hora_inicio))
                    ).first()
                    
                    if conflito:
                        flash('Já existe um horário agendado para este período!', 'error')
                        return render_template('horarios/criar.html', cadastros=cadastros, form_data=request.form)
                    
                    # Criar horário
                    horario = Horario(
                        cadastro_id=cadastro_id,
                        data=data,
                        hora_inicio=hora_inicio,
                        hora_fim=hora_fim,
                        descricao=request.form.get('descricao'),
                        status=request.form.get('status', 'agendado'),
                        tipo_servico=request.form.get('tipo_servico'),
                        prioridade=request.form.get('prioridade', 'normal')
                    )
                    
                    db.session.add(horario)
                    db.session.commit()
                    
                    flash('Horário agendado com sucesso!', 'success')
                    return redirect(url_for('listar_horarios'))
                    
                except ValueError as e:
                    flash('Formato de data ou hora inválido!', 'error')
                except Exception as e:
                    flash(f'Erro ao criar horário: {str(e)}', 'error')
                
                return render_template('horarios/criar.html', cadastros=cadastros, form_data=request.form)
            
            # GET - Mostrar formulário
            hoje = date.today()
            eventos_calendario = Horario.query.filter(Horario.data >= hoje).limit(10).all()
            
            return render_template('horarios/criar.html', 
                                 cadastros=cadastros, 
                                 hoje=hoje.strftime('%Y-%m-%d'),
                                 eventos_calendario=eventos_calendario)
    
    @app.route('/horarios/<int:id>')
    def visualizar_horario(id):
        with app.app_context():
            horario = Horario.query.get_or_404(id)
            
            # Calcular duração
            inicio = horario.hora_inicio
            fim = horario.hora_fim
            duracao_min = (fim.hour * 60 + fim.minute) - (inicio.hour * 60 + inicio.minute)
            horas = duracao_min // 60
            minutos = duracao_min % 60
            duracao = f"{horas}h {minutos}min" if horas > 0 else f"{minutos}min"
            
            # Histórico
            historico = [
                {'titulo': 'Criação do Agendamento', 'descricao': 'Agendamento criado pelo sistema', 
                 'data': horario.data_criacao, 'cor': 'bg-success', 'usuario': 'Sistema'}
            ]
            
            if horario.data_atualizacao:
                historico.append({'titulo': 'Atualização', 'descricao': 'Dados do agendamento atualizados', 
                                'data': horario.data_atualizacao, 'cor': 'bg-info', 'usuario': 'Sistema'})
            
            # Próximos agendamentos do mesmo cliente
            hoje = date.today()
            proximos_agendamentos = Horario.query.filter(
                Horario.cadastro_id == horario.cadastro_id,
                Horario.id != id,
                Horario.data >= hoje
            ).order_by(Horario.data, Horario.hora_inicio).limit(3).all()
            
            # Último agendamento do cliente
            ultimo_agendamento = Horario.query.filter(
                Horario.cadastro_id == horario.cadastro_id,
                Horario.id != id
            ).order_by(Horario.data.desc(), Horario.hora_inicio.desc()).first()
            
            # Total de agendamentos do cliente
            total_agendamentos_cliente = Horario.query.filter_by(cadastro_id=horario.cadastro_id).count()
            
            return render_template('horarios/visualizar.html', 
                                 horario=horario, 
                                 duracao=duracao,
                                 historico=historico,
                                 hoje=hoje,
                                 proximos_agendamentos=proximos_agendamentos,
                                 ultimo_agendamento=ultimo_agendamento.data if ultimo_agendamento else None,
                                 proximos_cliente=total_agendamentos_cliente - 1,
                                 agora=datetime.now())
    
    @app.route('/horarios/<int:id>/editar', methods=['GET', 'POST'])
    def editar_horario(id):
        
        horario = Horario.query.get_or_404(id)
        cadastros = Cadastro.query.order_by(Cadastro.nome).all()
        
        if request.method == 'POST':
            try:
                # Atualizar campos apenas se fornecidos
                if 'cadastro_id' in request.form and request.form['cadastro_id']:
                    horario.cadastro_id = int(request.form['cadastro_id'])
                
                if 'data' in request.form and request.form['data']:
                    nova_data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
                    if nova_data < date.today():
                        flash('Não é possível agendar para datas passadas!', 'error')
                        return render_template('horarios/editar.html', 
                                            horario=horario, 
                                            cadastros=cadastros, 
                                            form_data=request.form,
                                            agora=datetime.now())
                    horario.data = nova_data
                
                if 'hora_inicio' in request.form and request.form['hora_inicio']:
                    horario.hora_inicio = datetime.strptime(request.form['hora_inicio'], '%H:%M').time()
                
                if 'hora_fim' in request.form and request.form['hora_fim']:
                    horario.hora_fim = datetime.strptime(request.form['hora_fim'], '%H:%M').time()
                
                # Validar horários
                if horario.hora_fim <= horario.hora_inicio:
                    flash('A hora de término deve ser posterior à hora de início!', 'error')
                    return render_template('horarios/editar.html', 
                                        horario=horario, 
                                        cadastros=cadastros, 
                                        form_data=request.form,
                                        agora=datetime.now())
                
                # Verificar conflitos (exceto o próprio horário)
                conflito = Horario.query.filter(
                    Horario.data == horario.data,
                    Horario.id != id,
                    Horario.cadastro_id == horario.cadastro_id,
                    ((Horario.hora_inicio < horario.hora_fim) & (Horario.hora_fim > horario.hora_inicio))
                ).first()
                
                if conflito:
                    flash('Já existe outro horário agendado para este período!', 'error')
                    return render_template('horarios/editar.html', 
                                        horario=horario, 
                                        cadastros=cadastros, 
                                        form_data=request.form,
                                        agora=datetime.now())
                
                # Atualizar outros campos
                if 'descricao' in request.form:
                    horario.descricao = request.form['descricao']
                
                if 'status' in request.form:
                    horario.status = request.form['status']
                
                if 'tipo_servico' in request.form:
                    horario.tipo_servico = request.form['tipo_servico']
                
                if 'prioridade' in request.form:
                    horario.prioridade = request.form['prioridade']
                
                db.session.commit()
                
                flash('Horário atualizado com sucesso!', 'success')
                return redirect(url_for('visualizar_horario', id=id))
                
            except ValueError as e:
                flash('Formato de data ou hora inválido!', 'error')
                return render_template('horarios/editar.html', 
                                    horario=horario, 
                                    cadastros=cadastros, 
                                    form_data=request.form,
                                    agora=datetime.now())
            except Exception as e:
                flash(f'Erro ao atualizar horário: {str(e)}', 'error')
                return render_template('horarios/editar.html', 
                                    horario=horario, 
                                    cadastros=cadastros, 
                                    form_data=request.form,
                                    agora=datetime.now())
        
        # GET - Mostrar formulário
        return render_template('horarios/editar.html', 
                            horario=horario, 
                            cadastros=cadastros,
                            agora=datetime.now())
    
    @app.route('/horarios/<int:id>/deletar', methods=['POST'])
    def deletar_horario(id):
        try:
            with app.app_context():
                horario = Horario.query.get_or_404(id)
                db.session.delete(horario)
                db.session.commit()
                
                flash('Horário deletado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao deletar horário: {str(e)}', 'error')
        
        return redirect(url_for('listar_horarios'))
    
    # ========== EXPORTAÇÃO CSV ==========
    
    @app.route('/exportar/cadastros/csv')
    def exportar_cadastros_csv():
        """Exporta todos os cadastros para CSV"""
        with app.app_context():
            # Criar CSV em memória
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Cabeçalho
            writer.writerow(['ID', 'Nome', 'Email', 'Telefone', 'Documento', 'Data Cadastro'])
            
            # Dados
            cadastros = Cadastro.query.order_by(Cadastro.nome).all()
            for cad in cadastros:
                writer.writerow([
                    cad.id,
                    cad.nome,
                    cad.email,
                    cad.telefone or '',
                    cad.documento or '',
                    cad.data_criacao.strftime('%d/%m/%Y %H:%M')
                ])
            
            # Configurar resposta
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename=cadastros.csv'
            response.headers['Content-type'] = 'text/csv'
            
            return response
    
    @app.route('/exportar/horarios/csv')
    def exportar_horarios_csv():
        """Exporta todos os horários para CSV"""
        with app.app_context():
            output = io.StringIO()
            writer = csv.writer(output)
            
            writer.writerow(['ID', 'Cliente', 'Email Cliente', 'Data', 'Hora Início', 'Hora Fim', 'Duração', 'Serviço', 'Status', 'Prioridade'])
            
            horarios = Horario.query.order_by(Horario.data, Horario.hora_inicio).all()
            for hor in horarios:
                # Calcular duração
                inicio = hor.hora_inicio
                fim = hor.hora_fim
                duracao_min = (fim.hour * 60 + fim.minute) - (inicio.hour * 60 + inicio.minute)
                horas = duracao_min // 60
                minutos = duracao_min % 60
                duracao = f"{horas}h{minutos}min" if horas > 0 else f"{minutos}min"
                
                writer.writerow([
                    hor.id,
                    hor.cadastro.nome,
                    hor.cadastro.email,
                    hor.data.strftime('%d/%m/%Y'),
                    hor.hora_inicio.strftime('%H:%M'),
                    hor.hora_fim.strftime('%H:%M'),
                    duracao,
                    hor.descricao or '',
                    hor.status,
                    hor.prioridade or 'normal'
                ])
            
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename=horarios.csv'
            response.headers['Content-type'] = 'text/csv'
            
            return response
    
    @app.route('/exportar/relatorio/csv')
    def exportar_relatorio_csv():
        """Exporta relatório com filtros de data"""
        try:
            data_inicio = request.args.get('data_inicio', '')
            data_fim = request.args.get('data_fim', '')
            
            if not data_inicio or not data_fim:
                flash('Datas de início e fim são obrigatórias para o relatório!', 'error')
                return redirect(url_for('listar_horarios'))
            
            inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            
            with app.app_context():
                horarios = Horario.query.filter(
                    Horario.data >= inicio,
                    Horario.data <= fim
                ).order_by(Horario.data, Horario.hora_inicio).all()
                
                output = io.StringIO()
                writer = csv.writer(output)
                
                writer.writerow(['RELATÓRIO DE AGENDAMENTOS', f'Período: {data_inicio} até {data_fim}'])
                writer.writerow([])  # Linha vazia
                writer.writerow(['ID', 'Cliente', 'Data', 'Hora Início', 'Hora Fim', 'Serviço', 'Status', 'Prioridade'])
                
                for hor in horarios:
                    writer.writerow([
                        hor.id,
                        hor.cadastro.nome,
                        hor.data.strftime('%d/%m/%Y'),
                        hor.hora_inicio.strftime('%H:%M'),
                        hor.hora_fim.strftime('%H:%M'),
                        hor.descricao or '',
                        hor.status,
                        hor.prioridade or 'normal'
                    ])
                
                # Estatísticas
                total = len(horarios)
                writer.writerow([])
                writer.writerow(['ESTATÍSTICAS DO PERÍODO'])
                writer.writerow([f'Total de agendamentos: {total}'])
                
                # Contar por status
                status_count = {}
                for h in horarios:
                    status_count[h.status] = status_count.get(h.status, 0) + 1
                
                for status, count in status_count.items():
                    writer.writerow([f'{status}: {count}'])
                
                output.seek(0)
                response = make_response(output.getvalue())
                filename = f'relatorio_{data_inicio}_{data_fim}.csv'
                response.headers['Content-Disposition'] = f'attachment; filename={filename}'
                response.headers['Content-type'] = 'text/csv'
                
                return response
                
        except ValueError:
            flash('Formato de data inválido. Use YYYY-MM-DD', 'error')
            return redirect(url_for('listar_horarios'))
        except Exception as e:
            flash(f'Erro ao gerar relatório: {str(e)}', 'error')
            return redirect(url_for('listar_horarios'))
    
    # API para relatórios
    @app.route('/api/relatorio')
    def relatorio():
        try:
            data_inicio = request.args.get('data_inicio', '')
            data_fim = request.args.get('data_fim', '')
            
            if not data_inicio or not data_fim:
                return jsonify({'error': 'Datas de início e fim são obrigatórias'}), 400
            
            inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            
            with app.app_context():
                horarios = Horario.query.filter(
                    Horario.data >= inicio,
                    Horario.data <= fim
                ).order_by(Horario.data, Horario.hora_inicio).all()
                
                horarios_dict = [h.to_dict() for h in horarios]
                
                # Estatísticas
                total_agendamentos = len(horarios)
                total_clientes = len(set([h.cadastro_id for h in horarios]))
                status_count = {}
                for h in horarios:
                    status_count[h.status] = status_count.get(h.status, 0) + 1
                
                return jsonify({
                    'success': True,
                    'message': f'Relatório gerado para o período {data_inicio} até {data_fim}',
                    'data': horarios_dict,
                    'total': total_agendamentos,
                    'estatisticas': {
                        'total_agendamentos': total_agendamentos,
                        'total_clientes': total_clientes,
                        'status': status_count
                    }
                })
                
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao gerar relatório: {str(e)}'}), 500
    
    return app

# Criar aplicação
app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Sistema de Agendamento Web Iniciando...")
    print("🌐 Acesse: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)