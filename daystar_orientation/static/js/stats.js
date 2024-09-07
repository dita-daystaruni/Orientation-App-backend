document.getElementById('courseSelect').addEventListener('change', function() {
    let selectedCourse = this.value;
    window.location.href = '?course=' + selectedCourse;
});