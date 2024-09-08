// static/js/faqs-validation.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            const question = document.querySelector('input[name="question"]').value.trim();
            const answer = document.querySelector('textarea[name="answer"]').value.trim();
            const errorMsg = document.getElementById('error-message');
            
            // Clear previous error messages
            if (errorMsg) {
                errorMsg.remove();
            }
            
            // Validate fields
            if (!question || !answer) {
                event.preventDefault();
                const error = document.createElement('div');
                error.id = 'error-message';
                error.style.color = 'red';
                error.textContent = 'Both question and answer fields are required.';
                form.insertBefore(error, form.firstChild);
            }
        });
    }
});
