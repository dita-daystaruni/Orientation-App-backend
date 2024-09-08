// static/js/courses-validation.js

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function(event) {
        // Get form field values
        const firstName = document.getElementById('firstName').value.trim();
        const lastName = document.getElementById('lastName').value.trim();
        const position = document.getElementById('position').value.trim();
        const phoneNumber = document.getElementById('phoneNumber').value.trim();
        const email = document.getElementById('email').value.trim();
        const course = document.getElementById('course').value;

        // Clear previous error messages
        const errorMsg = document.getElementById('error-message');
        if (errorMsg) {
            errorMsg.style.display = 'none';
        }

        // Check if required fields are filled
        if (!firstName || !lastName || !position || !phoneNumber || !email || !course) {
            event.preventDefault();
            const error = document.createElement('div');
            error.id = 'error-message';
            error.style.color = 'red';
            error.textContent = 'Please fill out all fields.';
            document.querySelector('.btn-container').insertBefore(error, document.querySelector('.btn-container').firstChild);
            return;
        }

        // Validate email format
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            event.preventDefault();
            const error = document.createElement('div');
            error.id = 'error-message';
            error.style.color = 'red';
            error.textContent = 'Please enter a valid email address.';
            document.querySelector('.btn-container').insertBefore(error, document.querySelector('.btn-container').firstChild);
            return;
        }

        // Validate phone number format (simple check, you might need a more complex pattern)
        const phonePattern = /^\+2547\d{8}$/;
        if (!phonePattern.test(phoneNumber)) {
            event.preventDefault();
            const error = document.createElement('div');
            error.id = 'error-message';
            error.style.color = 'red';
            error.textContent = 'Please enter a valid phone number (e.g., +2547 12 345 678).';
            document.querySelector('.btn-container').insertBefore(error, document.querySelector('.btn-container').firstChild);
        }
    });
});
