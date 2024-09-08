function getRandomColor() {
    const colors = ['#D19955', '#317D89', '#6C757D', '#F85A40', '#17A2B8'];
    return colors[Math.floor(Math.random() * colors.length)];
}

// Function to generate initials and assign random background color
function setInitialsAndColor(notificationItem, name) {
    const initialsIcon = notificationItem.querySelector('.initials-icon');
    
    // Extract initials from the name
    const nameWords = name.split(" ");
    let initials = nameWords[0][0].toUpperCase();
    if (nameWords.length > 1) {
        initials += nameWords[1][0].toUpperCase();
    }
  
    // Set initials and random background color
    initialsIcon.setAttribute('data-initials', initials);
    initialsIcon.style.backgroundColor = getRandomColor();
}

// Iterate over all notifications and set initials for each
document.querySelectorAll('.notification-item').forEach((item) => {
    const username = item.querySelector('.sender-name').textContent;  // Pulling name from backend
    setInitialsAndColor(item, username);
});
