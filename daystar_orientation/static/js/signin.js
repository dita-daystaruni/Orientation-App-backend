document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.querySelector('.toggle-password');
    const passwordField = document.querySelector('#password');

    togglePassword.addEventListener('click', function () {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);

        this.classList.toggle('bi-eye');
        this.classList.toggle('bi-eye-slash');
    });
});
