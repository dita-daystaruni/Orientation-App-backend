// Helper function to generate random color
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
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

// Example usage
document.querySelectorAll('.notification-item').forEach((item, index) => {
    const username = "John Doe";  // Replace with actual username data
    setInitialsAndColor(item, username);
});
