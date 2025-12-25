// JavaScript-файл синхронизации статуса номеров

// Инициализация после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    // Проверить, является ли текущая страница страницей, требующей синхронизации статуса
    const currentPath = window.location.pathname;
    const syncPaths = ['/rooms/', '/room-status/', '/bookings/', '/check-in-out/'];
    
    if (syncPaths.some(path => currentPath.includes(path))) {
        // Запустить проверку синхронизации статуса
        startStatusSync();
    }
    
    // Проверить наличие сообщения об успешном выезде
    checkCheckoutSuccess();
});

// Запустить проверку синхронизации статуса
function startStatusSync() {
    // Проверять статус номеров каждые 10 секунд
    setInterval(function() {
        checkRoomStatusUpdates();
    }, 10000);
}

// Проверить обновления статуса номеров
function checkRoomStatusUpdates() {
    // Создать скрытый iframe для проверки статуса
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = '/room-status/';
    
    // После загрузки iframe проверить наличие обновлений
    iframe.onload = function() {
        // Здесь можно добавить более сложную логику сравнения статусов
        // Сейчас мы просто перезагружаем страницу для получения актуального статуса
        console.log('Проверка обновлений статуса номеров...');
    };
    
    document.body.appendChild(iframe);
    
    // Удалить iframe через 5 секунд
    setTimeout(function() {
        document.body.removeChild(iframe);
    }, 5000);
}

// Показать уведомление об обновлении статуса номеров
function showRoomStatusNotification(message) {
    // Создать элемент уведомления
    const notification = document.createElement('div');
    notification.className = 'alert alert-info alert-dismissible fade show position-fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Добавить на страницу
    document.body.appendChild(notification);
    
    // Автоматически закрыть через 5 секунд
    setTimeout(function() {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Проверить сообщение об успешном выезде и обновить страницу
function checkCheckoutSuccess() {
    // Проверить наличие параметра успешного выезда в URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('checkout_success')) {
        // Показать сообщение об успешном выезде
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success alert-dismissible fade show';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            Регистрация выезда прошла успешно! Статус комнаты обновлен.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Добавить сообщение в верхнюю часть страницы
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        }
        
        // Если на странице, требующей синхронизации статуса, обновить страницу для отображения нового статуса
        const currentPath = window.location.pathname;
        const syncPaths = ['/rooms/', '/room-status/', '/bookings/', '/check-in-out/'];
        if (syncPaths.some(path => currentPath.includes(path))) {
            // Использовать более короткую задержку для более быстрого отображения обновлений
            setTimeout(function() {
                window.location.reload();
            }, 1500);
        }
    }
}

// Добавить обработку после отправки формы для обеспечения правильного перенаправления после выезда
document.addEventListener('submit', function(event) {
    // Проверить, является ли форма формой выезда
    const form = event.target;
    const actionInput = form.querySelector('input[name="action"]');
    
    if (actionInput && actionInput.value === 'check_out') {
        // Добавить параметр перенаправления для обеспечения обновления страницы
        const redirectInput = form.querySelector('input[name="redirect_to"]');
        if (!redirectInput) {
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'redirect_to';
            hiddenInput.value = 'current_page';
            form.appendChild(hiddenInput);
        }
    }
});