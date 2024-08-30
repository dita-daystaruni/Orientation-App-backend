document.querySelectorAll('.faq-item .question').forEach(function(question) {
  question.addEventListener('click', function() {
      // Toggle the display of the answer
      const answer = question.nextElementSibling;
      const toggleIcon = question.querySelector('.question-toggle');

      if (answer.style.display === "none" || answer.style.display === "") {
          answer.style.display = "block";
          toggleIcon.classList.add('rotate');
      } else {
          answer.style.display = "none";
          toggleIcon.classList.remove('rotate');
      }
  });
});
