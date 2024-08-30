const timeElement = document.querySelector('.col-md-3 .main-sessions h6:first-child');
const currentDate = new Date();
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
const formattedDate = currentDate.toLocaleDateString('en-US', options);

timeElement.textContent = formattedDate;