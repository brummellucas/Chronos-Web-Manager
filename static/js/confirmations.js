// static/js/confirmations.js
// Funções de confirmação para o sistema

function confirmDeleteCadastro(id, nome) {
    if (confirm(`Tem certeza que deseja excluir o cadastro de "${nome}"?\n\nEsta ação não pode ser desfeita!`)) {
        document.getElementById(`delete-form-${id}`).submit();
    }
}

function confirmDeleteHorario(id, nomeCliente, data) {
    if (confirm(`Tem certeza que deseja excluir o horário de ${nomeCliente} em ${data}?\n\nEsta ação não pode ser desfeita!`)) {
        document.getElementById(`delete-horario-form-${id}`).submit();
    }
}

function confirmarExclusao(url, mensagem) {
    if (confirm(mensagem)) {
        // Criar formulário dinâmico para POST
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = url;
        form.style.display = 'none';
        
        // Adicionar CSRF token se existir
        const csrfToken = document.querySelector('meta[name="csrf-token"]');
        if (csrfToken) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'csrf_token';
            input.value = csrfToken.content;
            form.appendChild(input);
        }
        
        document.body.appendChild(form);
        form.submit();
    }
    return false;
}