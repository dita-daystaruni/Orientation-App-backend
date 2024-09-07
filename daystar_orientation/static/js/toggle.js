document.querySelectorAll('.faq-item .question').forEach(function(question) {
    question.addEventListener('click', function() {
        // Toggle the collapse of the answer section
        const answer = question.nextElementSibling;
        const toggleIcon = question.querySelector('.question-toggle');

        // Toggle the collapse class using Bootstrap's methods
        if (answer.classList.contains('show')) {
            toggleIcon.classList.remove('rotate');
        } else {
            toggleIcon.classList.add('rotate');
        }
    });
});

document.querySelectorAll('.answer .bi-chevron-up').forEach(function(chevronUp) {
    chevronUp.addEventListener('click', function() {
        const answer = chevronUp.closest('.answer');
        const questionToggleIcon = answer.previousElementSibling.querySelector('.question-toggle');

        // Collapse the answer section and rotate the chevron icon back
        answer.classList.remove('show');
        questionToggleIcon.classList.remove('rotate');
    });
});
