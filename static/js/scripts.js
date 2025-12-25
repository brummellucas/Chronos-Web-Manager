// ===== SISTEMA DE AGENDAMENTO - SCRIPT PRINCIPAL =====

// Document Ready
$(document).ready(function() {
    console.log('Sistema de Agendamento Web carregado!');
    
    // Inicializar componentes
    initComponents();
    
    // Configurar eventos
    setupEvents();
    
    // Carregar dados iniciais
    loadInitialData();
});

// ===== INICIALIZAÇÃO DE COMPONENTES =====
function initComponents() {
    // Inicializar DataTables
    if ($.fn.DataTable) {
        $('.data-table').each(function() {
            const table = $(this);
            const options = {
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/pt-BR.json'
                },
                pageLength: 10,
                responsive: true,
                autoWidth: false,
                order: [],
                dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>' +
                     '<"row"<"col-sm-12"tr>>' +
                     '<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
                initComplete: function() {
                    // Adicionar classe ao wrapper
                    $(this).closest('.dataTables_wrapper').addClass('table-responsive');
                }
            };
            
            table.DataTable(options);
        });
    }
    
    // Inicializar datepickers
    if (typeof flatpickr !== 'undefined') {
        // Date pickers
        $('input[type="date"]').each(function() {
            flatpickr(this, {
                dateFormat: "Y-m-d",
                locale: "pt",
                allowInput: true,
                disableMobile: true
            });
        });
        
        // Time pickers
        $('input[type="time"]').each(function() {
            flatpickr(this, {
                enableTime: true,
                noCalendar: true,
                dateFormat: "H:i",
                time_24hr: true,
                locale: "pt",
                allowInput: true,
                disableMobile: true
            });
        });
        
        // DateTime pickers
        $('.datetime-picker').each(function() {
            flatpickr(this, {
                enableTime: true,
                dateFormat: "Y-m-d H:i",
                time_24hr: true,
                locale: "pt",
                allowInput: true,
                disableMobile: true
            });
        });
    }
    
    // Inicializar selects com busca
    if ($.fn.select2) {
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%',
            placeholder: 'Selecione uma opção',
            allowClear: true,
            language: 'pt-BR'
        });
    }
    
    // Inicializar tooltips
    if ($.fn.tooltip) {
        $('[data-bs-toggle="tooltip"]').tooltip({
            trigger: 'hover',
            placement: 'top',
            delay: { show: 500, hide: 100 }
        });
    }
    
    // Inicializar popovers
    if ($.fn.popover) {
        $('[data-bs-toggle="popover"]').popover({
            trigger: 'hover',
            placement: 'top',
            html: true
        });
    }
    
    // Configurar máscaras de entrada
    setupInputMasks();
    
    // Inicializar validação de formulários
    setupFormValidation();
    
    // Configurar auto-refresh (se necessário)
    setupAutoRefresh();
}

// ===== CONFIGURAÇÃO DE EVENTOS =====
function setupEvents() {
    // Busca em tempo real
    $('#searchInput').on('input', debounce(function() {
        const searchTerm = $(this).val().trim();
        if (searchTerm.length >= 2 || searchTerm.length === 0) {
            performSearch(searchTerm);
        }
    }, 300));
    
    // Busca por Enter
    $('#searchInput').on('keypress', function(e) {
        if (e.which === 13) {
            performSearch($(this).val().trim());
        }
    });
    
    // Filtros de data
    $('.date-filter').on('change', function() {
        applyDateFilter();
    });
    
    // Exportação de dados
    $('.export-btn').on('click', function(e) {
        e.preventDefault();
        const format = $(this).data('format') || 'csv';
        exportData(format);
    });
    
    // Confirmação de exclusão
    $('.confirm-delete').on('click', function(e) {
        e.preventDefault();
        const url = $(this).attr('href');
        const message = $(this).data('message') || 'Tem certeza que deseja excluir este item?';
        confirmDelete(url, message);
    });
    
    // Modal de confirmação
    $(document).on('click', '[data-confirm]', function(e) {
        e.preventDefault();
        const message = $(this).data('confirm');
        const url = $(this).attr('href');
        
        Swal.fire({
            title: 'Confirmação',
            text: message,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#4361ee',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Sim, continuar',
            cancelButtonText: 'Cancelar',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = url;
            }
        });
    });
    
    // Alternância de status
    $('.toggle-status').on('change', function() {
        const itemId = $(this).data('id');
        const newStatus = $(this).is(':checked');
        toggleItemStatus(itemId, newStatus);
    });
    
    // Copiar para área de transferência
    $('.copy-to-clipboard').on('click', function() {
        const text = $(this).data('text') || $(this).text();
        copyToClipboard(text);
    });
    
    // Atualizar contador de caracteres
    $('textarea[maxlength]').on('input', function() {
        updateCharCounter($(this));
    });
    
    // Auto-complete para campos de busca
    setupAutocomplete();
    
    // Drag and drop para uploads
    setupDragAndDrop();
    
    // Notificações em tempo real
    setupRealTimeNotifications();
}

// ===== FUNÇÕES DE BUSCA E FILTRO =====
function performSearch(term) {
    // Mostrar loading
    showLoading('#searchResults');
    
    // Simular busca (substituir por chamada AJAX real)
    setTimeout(() => {
        // Aqui você faria uma chamada AJAX para buscar dados
        // Exemplo:
        /*
        $.ajax({
            url: '/api/search',
            method: 'GET',
            data: { q: term },
            success: function(data) {
                updateSearchResults(data);
            },
            error: function() {
                showError('Erro na busca');
            }
        });
        */
        
        hideLoading('#searchResults');
        
        // Atualizar contador
        const count = Math.floor(Math.random() * 50) + 1;
        $('#searchCount').text(count + ' resultados encontrados');
        
    }, 500);
}

function applyDateFilter() {
    const startDate = $('#startDate').val();
    const endDate = $('#endDate').val();
    
    if (!startDate || !endDate) {
        showWarning('Selecione um período válido');
        return;
    }
    
    // Redirecionar ou fazer chamada AJAX
    const url = new URL(window.location.href);
    url.searchParams.set('start_date', startDate);
    url.searchParams.set('end_date', endDate);
    window.location.href = url.toString();
}

// ===== FUNÇÕES DE FORMULÁRIO =====
function setupInputMasks() {
    // Máscara para telefone
    $('.phone-mask').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length > 10) {
            value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
        } else if (value.length > 6) {
            value = value.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
        } else if (value.length > 2) {
            value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
        } else if (value.length > 0) {
            value = value.replace(/^(\d*)/, '($1');
        }
        $(this).val(value);
    });
    
    // Máscara para CPF
    $('.cpf-mask').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length > 9) {
            value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2}).*/, '$1.$2.$3-$4');
        } else if (value.length > 6) {
            value = value.replace(/^(\d{3})(\d{3})(\d{0,3})/, '$1.$2.$3');
        } else if (value.length > 3) {
            value = value.replace(/^(\d{3})(\d{0,3})/, '$1.$2');
        }
        $(this).val(value);
    });
    
    // Máscara para CNPJ
    $('.cnpj-mask').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length > 12) {
            value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2}).*/, '$1.$2.$3/$4-$5');
        } else if (value.length > 8) {
            value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{0,4})/, '$1.$2.$3/$4');
        } else if (value.length > 5) {
            value = value.replace(/^(\d{2})(\d{3})(\d{0,3})/, '$1.$2.$3');
        } else if (value.length > 2) {
            value = value.replace(/^(\d{2})(\d{0,3})/, '$1.$2');
        }
        $(this).val(value);
    });
    
    // Máscara para moeda
    $('.currency-mask').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        value = (value / 100).toFixed(2) + '';
        value = value.replace(".", ",");
        value = value.replace(/(\d)(\d{3})(\d{3}),/g, "$1.$2.$3,");
        value = value.replace(/(\d)(\d{3}),/g, "$1.$2,");
        $(this).val('R$ ' + value);
    });
    
    // Máscara para CEP
    $('.cep-mask').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length > 5) {
            value = value.replace(/^(\d{5})(\d{3}).*/, '$1-$2');
        }
        $(this).val(value);
    });
}

function setupFormValidation() {
    // Validação customizada
    $.validator.addMethod("phoneBR", function(phone_number, element) {
        phone_number = phone_number.replace(/\s+/g, "");
        return this.optional(element) || phone_number.length > 9 &&
            phone_number.match(/^(?:(?:\+|00)?(55)\s?)?(?:\(?([1-9][0-9])\)?\s?)?(?:((?:9\d|[2-9])\d{3})\-?(\d{4}))$/);
    }, "Informe um telefone válido");
    
    $.validator.addMethod("cpf", function(cpf, element) {
        cpf = cpf.replace(/\D/g, '');
        return this.optional(element) || validateCPF(cpf);
    }, "Informe um CPF válido");
    
    // Aplicar validação aos formulários
    $('form.validate').each(function() {
        $(this).validate({
            rules: {
                telefone: { phoneBR: true },
                cpf: { cpf: true },
                email: { email: true }
            },
            messages: {
                nome: { required: "Campo obrigatório" },
                email: { 
                    required: "Campo obrigatório",
                    email: "Informe um e-mail válido"
                }
            },
            errorElement: 'span',
            errorClass: 'invalid-feedback',
            highlight: function(element) {
                $(element).addClass('is-invalid').removeClass('is-valid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid').addClass('is-valid');
            },
            errorPlacement: function(error, element) {
                error.insertAfter(element);
            }
        });
    });
}

function validateCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
    
    let soma = 0;
    let resto;
    
    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }
    
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.substring(9, 10))) return false;
    
    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }
    
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.substring(10, 11))) return false;
    
    return true;
}

// ===== FUNÇÕES DE INTERFACE =====
function showLoading(selector = 'body') {
    const loadingHtml = `
        <div class="spinner-container">
            <div class="spinner"></div>
        </div>
    `;
    $(selector).append(loadingHtml);
}

function hideLoading(selector = 'body') {
    $(selector).find('.spinner-container').remove();
}

function showSuccess(message, title = 'Sucesso!') {
    Swal.fire({
        icon: 'success',
        title: title,
        text: message,
        timer: 3000,
        showConfirmButton: false
    });
}

function showError(message, title = 'Erro!') {
    Swal.fire({
        icon: 'error',
        title: title,
        text: message,
        confirmButtonColor: '#4361ee'
    });
}

function showWarning(message, title = 'Atenção!') {
    Swal.fire({
        icon: 'warning',
        title: title,
        text: message,
        confirmButtonColor: '#4361ee'
    });
}

function showInfo(message, title = 'Informação') {
    Swal.fire({
        icon: 'info',
        title: title,
        text: message,
        confirmButtonColor: '#4361ee'
    });
}

function confirmDelete(url, message = 'Tem certeza que deseja excluir este item?') {
    Swal.fire({
        title: 'Confirmar Exclusão',
        text: message,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e63946',
        cancelButtonColor: '#4361ee',
        confirmButtonText: 'Sim, excluir!',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            // Enviar requisição DELETE
            $.ajax({
                url: url,
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                },
                success: function(response) {
                    showSuccess('Item excluído com sucesso!');
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                },
                error: function() {
                    showError('Erro ao excluir item');
                }
            });
        }
    });
}

function getCsrfToken() {
    return $('meta[name="csrf-token"]').attr('content') || 
           $('input[name="csrfmiddlewaretoken"]').val() ||
           '';
}

// ===== FUNÇÕES DE UTILIDADE =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Copiado para a área de transferência!');
    }).catch(err => {
        showError('Erro ao copiar texto');
    });
}

function updateCharCounter(textarea) {
    const maxLength = parseInt(textarea.attr('maxlength'));
    const currentLength = textarea.val().length;
    const counterId = textarea.attr('id') + '-counter';
    
    let counter = $('#' + counterId);
    if (counter.length === 0) {
        counter = $(`<small class="form-text text-muted char-counter" id="${counterId}"></small>`);
        textarea.after(counter);
    }
    
    counter.text(`${currentLength}/${maxLength} caracteres`);
    
    if (currentLength > maxLength * 0.9) {
        counter.addClass('text-warning');
        counter.removeClass('text-danger');
    } else if (currentLength > maxLength) {
        counter.addClass('text-danger');
        counter.removeClass('text-warning');
    } else {
        counter.removeClass('text-warning text-danger');
    }
}

// ===== FUNÇÕES DE DADOS =====
function loadInitialData() {
    // Carregar estatísticas
    loadStatistics();
    
    // Carregar notificações
    loadNotifications();
    
    // Carregar agenda do dia
    loadTodaySchedule();
}

function loadStatistics() {
    // Simular carregamento de estatísticas
    // Em produção, fazer chamada AJAX
    setTimeout(() => {
        const stats = {
            cadastros: 156,
            horarios: 42,
            disponibilidade: 78,
            receita: 12500
        };
        
        updateStatisticsDisplay(stats);
    }, 1000);
}

function updateStatisticsDisplay(stats) {
    $('#stat-cadastros').text(stats.cadastros);
    $('#stat-horarios').text(stats.horarios);
    $('#stat-disponibilidade').text(stats.disponibilidade + '%');
    $('#stat-receita').text('R$ ' + stats.receita.toLocaleString('pt-BR'));
}

// ===== FUNÇÕES DE NOTIFICAÇÃO =====
function setupRealTimeNotifications() {
    // Em produção, usar WebSockets ou Server-Sent Events
    // Exemplo com polling:
    setInterval(checkNotifications, 30000); // Verificar a cada 30 segundos
}

function checkNotifications() {
    $.get('/api/notifications/unread-count', function(count) {
        if (count > 0) {
            updateNotificationBadge(count);
            if (Notification.permission === "granted") {
                showDesktopNotification('Novas notificações', `Você tem ${count} nova(s) notificação(ões)`);
            }
        }
    });
}

function updateNotificationBadge(count) {
    const badge = $('#notificationBadge');
    if (count > 0) {
        badge.text(count).show();
    } else {
        badge.hide();
    }
}

function showDesktopNotification(title, body) {
    if (!("Notification" in window)) return;
    
    if (Notification.permission === "granted") {
        new Notification(title, { body: body, icon: '/static/favicon.ico' });
    } else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                new Notification(title, { body: body, icon: '/static/favicon.ico' });
            }
        });
    }
}

// ===== EXPORTAÇÃO DE DADOS =====
function exportData(format) {
    showLoading();
    
    // Em produção, fazer chamada AJAX para gerar o arquivo
    setTimeout(() => {
        hideLoading();
        
        let message = '';
        switch(format) {
            case 'csv':
                message = 'Arquivo CSV gerado com sucesso!';
                // Simular download
                const csvContent = "data:text/csv;charset=utf-8,";
                const encodedUri = encodeURI(csvContent);
                const link = document.createElement("a");
                link.setAttribute("href", encodedUri);
                link.setAttribute("download", "relatorio.csv");
                document.body.appendChild(link);
                link.click();
                break;
                
            case 'pdf':
                message = 'Arquivo PDF gerado com sucesso!';
                break;
                
            case 'excel':
                message = 'Arquivo Excel gerado com sucesso!';
                break;
        }
        
        showSuccess(message);
    }, 2000);
}

// ===== FUNÇÕES DE AGENDA =====
function setupDragAndDrop() {
    // Configurar drag and drop para uploads
    const dropZone = $('#dropZone');
    if (dropZone.length) {
        dropZone.on('dragover', function(e) {
            e.preventDefault();
            $(this).addClass('dragover');
        });
        
        dropZone.on('dragleave', function() {
            $(this).removeClass('dragover');
        });
        
        dropZone.on('drop', function(e) {
            e.preventDefault();
            $(this).removeClass('dragover');
            
            const files = e.originalEvent.dataTransfer.files;
            if (files.length) {
                handleFileUpload(files[0]);
            }
        });
    }
}

function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    $.ajax({
        url: '/api/upload',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'X-CSRFToken': getCsrfToken()
        },
        success: function(response) {
            showSuccess('Arquivo enviado com sucesso!');
        },
        error: function() {
            showError('Erro ao enviar arquivo');
        }
    });
}

// ===== INICIALIZAÇÃO FINAL =====
function setupAutoRefresh() {
    // Auto-refresh para páginas que precisam de dados em tempo real
    if ($('[data-auto-refresh]').length) {
        const interval = parseInt($('[data-auto-refresh]').data('refresh-interval')) || 30000;
        setInterval(() => {
            if (document.hasFocus()) {
                window.location.reload();
            }
        }, interval);
    }
}

function setupAutocomplete() {
    // Configurar auto-complete para campos de busca
    $('.autocomplete').each(function() {
        $(this).autocomplete({
            source: function(request, response) {
                $.ajax({
                    url: '/api/autocomplete',
                    data: { term: request.term, field: $(this).data('field') },
                    success: function(data) {
                        response(data);
                    }
                });
            },
            minLength: 2,
            select: function(event, ui) {
                $(this).val(ui.item.value);
                $(this).trigger('change');
            }
        });
    });
}

// ===== EXPORTAÇÃO DE FUNÇÕES GLOBAIS =====
// Disponibilizar funções importantes globalmente
window.Agendamento = {
    showSuccess: showSuccess,
    showError: showError,
    showWarning: showWarning,
    showInfo: showInfo,
    confirmDelete: confirmDelete,
    copyToClipboard: copyToClipboard,
    validateCPF: validateCPF,
    getCsrfToken: getCsrfToken,
    debounce: debounce
};

// Inicialização final
$(window).on('load', function() {
    console.log('Página completamente carregada');
    
    // Esconder preloader se existir
    $('.preloader').fadeOut(300, function() {
        $(this).remove();
    });
    
    // Animação de entrada
    $('.fade-in').css('opacity', 0).animate({ opacity: 1 }, 1000);
    $('.slide-in').css({ opacity: 0, transform: 'translateX(20px)' })
                  .animate({ opacity: 1, transform: 'translateX(0)' }, 1000);
});