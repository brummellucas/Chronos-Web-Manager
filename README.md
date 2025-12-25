# 🕒 Chronos Web Manager - Sistema de Agendamento MVC

O **Chronos Web Manager** é uma solução completa para gestão de horários e cadastros, desenvolvida para demonstrar a aplicação prática de padrões de projeto e arquitetura web moderna.

## 🚀 Tecnologias Utilizadas
* **Backend:** Python 3.13 com framework Flask
* **Banco de Dados:** SQLite (com suporte para migração PostgreSQL)
* **Frontend:** Bootstrap 5, FullCalendar (Agenda), e SweetAlert2
* **Arquitetura:** MVC (Model-View-Controller) e Repository Pattern

## 📋 Funcionalidades Principais
- **CRUD Completo:** Gestão de clientes e agendamentos
- **Agenda Interativa:** Visualização mensal e semanal integrada
- **Lógica de Negócio:** Prevenção de conflitos de horários e validação de datas
- **Dashboard:** Visão geral de estatísticas e disponibilidade

## ⚙️ Como Executar o Projeto
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`.
3. Ative o ambiente e instale as dependências: `pip install -r requirements.txt`.
4. Configure o arquivo `.env` com sua `SECRET_KEY`.
5. Execute a aplicação: `python app.py`.
