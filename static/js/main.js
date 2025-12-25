// Основной JavaScript файл для системы управления отелем

// Подтверждение удаления
function confirmAction(message) {
    return confirm(message || 'Вы уверены, что хотите выполнить это действие?');
}

// Инициализация после загрузки документа
document.addEventListener('DOMContentLoaded', function() {
    // Добавляем обработчики для кнопок удаления
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirmAction('Вы уверены, что хотите удалить этот элемент?')) {
                e.preventDefault();
            }
        });
    });
    
    // Автоматическое закрытие уведомлений через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.classList.contains('alert-dismissible')) {
                const closeBtn = alert.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                }
            }
        }, 5000);
    });
    
    // Подсветка активной ссылки в меню
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Проверка параметра успешного выезда и отображение уведомления
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('checkout_success')) {
        // Создание сообщения уведомления
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success alert-dismissible fade show';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            Регистрация выезда прошла успешно! Статус комнаты обновлен.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Добавление сообщения уведомления в верхнюю часть страницы
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        }
    }
});

// Функция для форматирования даты
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('ru-RU', options);
}

// Функция для проверки формы
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    }
    return true;
}

// Функция для отображения загрузки
function showLoading() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'block';
    }
}

// Функция для скрытия загрузки
function hideLoading() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
}