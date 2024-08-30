function toggleSearchInput() {
    const searchInput = document.getElementById('search-input');
    if (searchInput.classList.contains('d-none')) {
        searchInput.classList.remove('d-none');
        setTimeout(() => searchInput.classList.add('active'), 10); // Add a slight delay to trigger the transition
    } else {
        searchInput.classList.remove('active');
        setTimeout(() => searchInput.classList.add('d-none'), 300); // Wait for the transition to finish before hiding
    }
}
