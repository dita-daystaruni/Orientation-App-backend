// static/js/notification-validation.js

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function(event) {
        // Get form field values
        const title = document.getElementById('notificationTitle').value.trim();
        const description = document.getElementById('notificationDescription').value.trim();
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        
        // Clear previous error messages
        const errorMsg = document.getElementById('error-message');
        if (errorMsg) {
            errorMsg.style.display = 'none';
        }

        // Check if title and description are filled
        if (!title || !description) {
            event.preventDefault();
            const error = document.createElement('div');
            error.id = 'error-message';
            error.style.color = 'red';
            error.textContent = 'Please fill out both the title and description fields.';
            document.querySelector('.drop-container').insertBefore(error, document.querySelector('.dropdown'));
            return;
        }

        // Check if at least one checkbox is selected
        const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
        if (!isChecked) {
            event.preventDefault();
            const error = document.createElement('div');
            error.id = 'error-message';
            error.style.color = 'red';
            error.textContent = 'Please select at least one category to view the notification.';
            document.querySelector('.drop-container').insertBefore(error, document.querySelector('.dropdown'));
        }
    });
});
