# 🕒 Chronos Web Manager - Sistema de Gestão de Agendamentos

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-purple?logo=bootstrap)
![SQLite](https://img.shields.io/badge/SQLite-3.40-lightblue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Sistema web completo para gestão de agendamentos com arquitetura MVC e interface moderna**

</div>

---

## 📋 **Índice**
- [✨ Características](#-características)
- [🏗️ Arquitetura](#️-arquitetura)
- [🚀 Tecnologias](#-tecnologias)
- [📦 Instalação](#-instalação)
- [🔧 Configuração](#-configuração)
- [🎯 Funcionalidades](#-funcionalidades)
- [📊 Demonstração](#-demonstração)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🤝 Contribuindo](#-contribuindo)
- [📄 Licença](#-licença)
- [👨‍💻 Autor](#-autor)

---

## ✨ **Características**

| Recurso | Descrição | Status |
|---------|-----------|--------|
| ✅ **CRUD Completo** | Gestão total de clientes e agendamentos | Implementado |
| ✅ **Dashboard Interativo** | Estatísticas em tempo real | Implementado |
| ✅ **Calendário Dinâmico** | Visualização FullCalendar integrada | Implementado |
| ✅ **Validação Inteligente** | Prevenção de conflitos de horário | Parcial |
| ✅ **Interface Responsiva** | Design adaptável a todos dispositivos | Implementado |
| ✅ **Busca e Filtros** | Localização rápida de dados | Implementado |
| ✅ **Exportação de Dados** | Relatórios em múltiplos formatos | Parcial |

---

## 🏗️ **Arquitetura**

```text
📁 Chronos Web Manager (Padrão MVC + Repository)
├── 📁 models/           # Modelos de dados (SQLAlchemy ORM)
│   ├── Cadastro.py     # Entidade Cliente/Pessoa
│   └── Horario.py      # Entidade Agendamento
├── 📁 repositories/     # Repository Pattern (Acesso a dados)
│   ├── Database.py     # Gerenciamento de conexões
│   ├── CadastroRepository.py
│   └── HorarioRepository.py
├── 📁 controllers/      # Lógica de negócio
│   ├── CadastroController.py
│   └── HorarioController.py
├── 📁 templates/        # Views (Jinja2 Templates)
│   ├── base.html       # Layout principal
│   ├── cadastros/      # CRUD de cadastros
│   └── horarios/       # CRUD de agendamentos
├── 📁 static/           # Assets estáticos
│   ├── css/style.css   # Estilos customizados
│   └── js/scripts.js   # JavaScript interativo
└── 🚀 app.py           # Aplicação Flask principal
```

**Padrões de Projeto Implementados:**
- **MVC (Model-View-Controller)**: Separação clara de responsabilidades
- **Repository Pattern**: Abstração de acesso a dados
- **Singleton**: Conexão única com banco de dados
- **Factory Method**: Criação de objetos de domínio

---

## 🚀 **Tecnologias**

### **Backend**
- **Python 3.13** - Linguagem principal
- **Flask 3.0** - Framework web minimalista
- **SQLAlchemy 3.0** - ORM para persistência de dados
- **Flask-SQLAlchemy** - Integração Flask + SQLAlchemy

### **Frontend**
- **Bootstrap 5.1** - Framework CSS responsivo
- **FullCalendar 5.10** - Biblioteca de calendário interativo
- **SweetAlert2** - Alertas modais elegantes
- **DataTables** - Tabelas interativas com filtros
- **Flatpickr** - Seletores de data/hora modernos

### **Banco de Dados**
- **SQLite 3** - Banco leve e embutido (desenvolvimento)
- **PostgreSQL** - Compatível para produção

### **Ferramentas**
- **Git** - Controle de versão
- **Virtualenv** - Ambientes virtuais Python
- **Python-dotenv** - Gerenciamento de variáveis

---

## 📦 **Instalação**

### **Pré-requisitos**
- Python 3.8 ou superior
- Git
- Navegador moderno

### **Passo a Passo**

```bash
# 1. Clone o repositório
git clone https://github.com/brummellucas/Chronos-Web-Manager.git
cd chronos-web-manager

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# 6. Execute a aplicação
python app.py

# 7. Acesse no navegador
# http://localhost:5000
```

### **Configuração Rápida (.env)**
```env
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=sqlite:///agendamento.db
```

---

## 🔧 **Configuração**

### **Banco de Dados**
O sistema usa SQLite por padrão. Para usar PostgreSQL:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/chronos_db
```

### **Personalização**
Edite `config.py` para:
- Alterar configurações do Flask
- Definir timezone
- Configurar logging
- Definir limites de upload

---

## 🎯 **Funcionalidades**

### **1. Gestão de Cadastros**
- ✅ **Criação**: Registro completo com validações
- ✅ **Listagem**: Tabela paginada com busca em tempo real
- ✅ **Visualização**: Perfil detalhado com histórico
- 🔄 **Edição**: Atualização segura
- 🔄 **Exclusão**: Remoção com confirmação

### **2. Sistema de Agendamentos**
- ✅ **Agendamento Inteligente**: Prevenção de conflitos
- ✅ **Calendário Interativo**: Visualização mensal/semanal
- ✅ **Validações**: Data futura, horário válido
- ✅ **Status**: Agendado → Confirmado → Realizado
- ✅ **Reagendamento**: Transferência fácil

### **3. Dashboard Analytics**
- ✅ **Estatísticas**: Totais e disponibilidade
- ✅ **Agenda do Dia**: Próximos compromissos
- ✅ **Calendário**: Visão geral do mês
- 🔄 **Gráficos**: Visualização de ocupação (planejado)

### **4. Recursos Avançados**
- ✅ **Filtros**: Por data, cliente, status
- ✅ **Busca**: Textual em múltiplos campos
- 🔄 **Responsividade**: Mobile/Tablet/Desktop
- 🔄 **Exportação**: CSV, PDF (parcial)

---

## 📊 **Demonstração**

### **Fluxo de Trabalho**
1. **Cadastre um cliente** com informações completas
2. **Agende um horário** verificando disponibilidade
3. **Visualize no calendário** a distribuição de compromissos
4. **Filtre e busque** agendamentos por diversos critérios
5. **Acompanhe estatísticas** no dashboard principal

### **API Endpoints**
```http
GET    /api/relatorio?data_inicio=2024-01-01&data_fim=2024-01-31
POST   /cadastros/novo
PUT    /cadastros/{id}/editar
DELETE /cadastros/{id}/deletar
```

---

## 📁 **Estrutura do Projeto**

```text
chronos-web-manager/
├── 📁 static/
│   ├── 📁 css/
│   │   └── style.css        # Estilos customizados
│   └── 📁 js/
│       └── scripts.js       # JavaScript interativo
├── 📁 templates/
│   ├── base.html            # Layout base
│   ├── index.html           # Dashboard
│   ├── 📁 cadastros/        # CRUD de cadastros
│   └── 📁 horarios/         # CRUD de agendamentos
├── 📁 models/
│   ├── __init__.py
│   ├── Cadastro.py          # Modelo Cadastro
│   └── Horario.py           # Modelo Horario
├── 📁 repositories/
│   ├── __init__.py
│   ├── Database.py          # Gerenciamento de conexão
│   ├── CadastroRepository.py
│   └── HorarioRepository.py
├── 📁 controllers/
│   ├── __init__.py
│   ├── CadastroController.py
│   └── HorarioController.py
├── 📄 .env.example          # Template de variáveis
├── 📄 .gitignore            # Arquivos ignorados
├── 📄 requirements.txt      # Dependências Python
├── 📄 config.py             # Configurações
├── 📄 app.py               # Aplicação Flask
├── 📄 LICENSE              # Licença MIT
└── 📄 README.md            # Este arquivo
```

---

## 🤝 **Contribuindo**

Contribuições são bem-vindas! Siga estes passos:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature
3. **Commit** suas mudanças
4. **Push** para a branch
5. Abra um **Pull Request**

### **Guidelines**
- Siga o padrão PEP 8 para Python
- Use type hints quando possível
- Documente funções complexas
- Teste suas alterações

### **Roadmap**
- [ ] Autenticação de usuários
- [ ] Notificações por email
- [ ] API REST completa
- [ ] Multi-tenancy
- [ ] Relatórios avançados

---

## 📄 **Licença**

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 👨‍💻 **Autor**

**Brummel Lucas Silva da Cunha** - Desenvolvedor.

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/brummellucas)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/brummellucas/)

</div>

---

<div align="center">

### ⭐ **Se este projeto te ajudou, deixe uma estrela no GitHub!**

**"Gerencie seu tempo, gerencie sua vida."**

</div>

---

## 🚀 **Execução Rápida**

Para executar rapidamente:

```bash
# Clone, configure e execute em 3 comandos:
git clone https://github.com/seu-usuario/chronos-web-manager.git
cd chronos-web-manager && pip install -r requirements.txt && python app.py
```

O sistema estará disponível em: **http://localhost:5000**

Usuário de demonstração:
- Email: admin@chronos.com
- Senha: demo123 (se implementar login)

---

## 🔍 **Para Recrutadores**

Este projeto demonstra:

### **Habilidades Técnicas:**
- ✅ Arquitetura MVC bem implementada
- ✅ Padrões de projeto (Repository, Singleton)
- ✅ API RESTful design
- ✅ Frontend moderno com Bootstrap
- ✅ Banco de dados relacional com ORM
- ✅ Validações e lógica de negócio


### **Pontos Destaque:**
1. **Dashboard interativo** com estatísticas em tempo real
2. **Calendário profissional** com FullCalendar
3. **Sistema de agendamento** com prevenção de conflitos
4. **CRUD completo** com validações robustas
5. **Design responsivo** para todos dispositivos


## 🎓 **Projeto Acadêmico**

Este projeto foi desenvolvido como parte do curso de **Tecnologia análise e Desenvolvimento de Sistemas**, demonstrando:

- Aplicação prática de padrões de arquitetura
- Desenvolvimento full-stack
- Gestão de projeto do zero
- Documentação profissional
- Boas práticas de desenvolvimento

