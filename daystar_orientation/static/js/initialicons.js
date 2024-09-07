function getRandomColor() {
    const colors = ['#D19955', '#317D89'];
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

// Example usage: This will be tied to the Django rendered elements
document.querySelectorAll('.notification-item').forEach((item) => {
    const username = item.querySelector('.sender-name').innerText;
    setInitialsAndColor(item, username);
});
