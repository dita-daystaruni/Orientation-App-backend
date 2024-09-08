function filterTable() {
    const input = document.getElementById('search-input').value.toLowerCase();
    const table = document.getElementById('students-table');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {  // Start from 1 to skip the header row
        const admissionCell = rows[i].getElementsByTagName('td')[1];  // Admission column index
        if (admissionCell) {
            const admissionNumber = admissionCell.textContent.toLowerCase();
            if (admissionNumber.includes(input)) {
                rows[i].style.display = '';  // Show row
            } else {
                rows[i].style.display = 'none';  // Hide row
            }
        }
    }
}
