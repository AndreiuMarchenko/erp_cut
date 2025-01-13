function showAlert(type, message) {
    // Створюємо елемент алерту
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
         <i class="bi ${type === 'danger' ? 'bi-x-circle' : 'bi-check-circle'} alert-icon"></i>
        ${message}
    `;
    // Стилі для фіксованої позиції
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '90px'; // Відстань від верху
    alertDiv.style.left = '50%';
    alertDiv.style.transform = 'translateX(-50%)';
    alertDiv.style.zIndex = '1050'; // Високий z-index для накладання поверх інших елементів
    alertDiv.style.width = '400px'; // Фіксована ширина
    alertDiv.style.textAlign = 'center';

    // Додаємо алерт в початок тіла документа
    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.classList.remove('show'); 
        alertDiv.addEventListener('transitionend', () => alertDiv.remove()); // Видаляє елемент після завершення анімації
    }, 4000);
}