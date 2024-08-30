document.getElementById('current-date').innerText = new Date().toLocaleDateString('en-US', {
weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
});