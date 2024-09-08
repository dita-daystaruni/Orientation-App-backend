document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('studentForm').addEventListener('submit', function (event) {
        let isValid = true;

        // Get all the input fields
        const firstName = document.getElementById('firstName');
        const lastName = document.getElementById('lastName');
        const admissionNumber = document.getElementById('admissionNumber');
        const phoneNumber = document.getElementById('phoneNumber');
        const email = document.getElementById('email');
        const password = document.getElementById('password');

        // Clear previous error messages
        document.querySelectorAll('.error-message').forEach(function (msg) {
            msg.style.display = 'none';
        });

        // Validate first name
        if (firstName.value.trim() === '') {
            isValid = false;
            firstName.nextElementSibling.style.display = 'block';
        }

        // Validate last name
        if (lastName.value.trim() === '') {
            isValid = false;
            lastName.nextElementSibling.style.display = 'block';
        }

        // Validate admission number
        if (admissionNumber.value.trim() === '') {
            isValid = false;
            admissionNumber.nextElementSibling.style.display = 'block';
        }

        // Validate phone number
        if (phoneNumber.value.trim() === '') {
            isValid = false;
            phoneNumber.nextElementSibling.style.display = 'block';
        }

        // Validate email
        if (email.value.trim() === '') {
            isValid = false;
            email.nextElementSibling.style.display = 'block';
        }

        // Validate password
        if (password.value.trim() === '') {
            isValid = false;
            password.nextElementSibling.style.display = 'block';
        }

        // Validate radio buttons
        const genderRadios = document.getElementsByName('gender');
        const campusRadios = document.getElementsByName('campus');
        const userTypeRadios = document.getElementsByName('user_type');

        if (![...genderRadios].some(radio => radio.checked)) {
            isValid = false;
            document.querySelector('label[for="gender"]').nextElementSibling.style.display = 'block';
        }

        if (![...campusRadios].some(radio => radio.checked)) {
            isValid = false;
            document.querySelector('label[for="campus"]').nextElementSibling.style.display = 'block';
        }

        if (![...userTypeRadios].some(radio => radio.checked)) {
            isValid = false;
            document.querySelector('label[for="user_type"]').nextElementSibling.style.display = 'block';
        }

        // Prevent form submission if validation fails
        if (!isValid) {
            event.preventDefault();
        }
    });
});
