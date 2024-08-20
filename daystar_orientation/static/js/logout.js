
  // Function to handle log out
  function handleLogout() {
    // Clear session storage or local storage (if used)
    sessionStorage.clear();
    localStorage.clear();

    // Optionally: Inform the user they are logging out
    alert("You have been logged out successfully.");

    // Redirect to the login page (or any other page)
    window.location.href = "signin.html";  // Change to the appropriate login page
  }

  // Event listener for the log-out button
  document.getElementById("logout-btn").addEventListener("click", function(event) {
    event.preventDefault();  // Prevent the default link behavior
    handleLogout();
  });
