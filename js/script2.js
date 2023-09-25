document.addEventListener("DOMContentLoaded", function() {
    // Select the course card button and the options
    const courseCardBtn = document.querySelector('.course-card-btn');
    const courseCardOptions = document.querySelector('.course-card-options');
    const courseOptions = document.querySelectorAll('.course-option');
    const confirmBtn = document.querySelector('.confirm-btn');

    // Event listener to toggle the dropdown
    courseCardBtn.addEventListener('click', function() {
        if (courseCardOptions.style.display === 'none' || courseCardOptions.style.display === '') {
            courseCardOptions.style.display = 'block';
        } else {
            courseCardOptions.style.display = 'none';
        }
    });

    // Close the dropdown when clicked outside
    document.addEventListener('click', function(event) {
        if (!courseCardBtn.contains(event.target)) {
            courseCardOptions.style.display = 'none';
        }
    });

    // Update the button text when an option is selected
    courseOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            courseCardBtn.innerHTML = `${option.textContent} <i class="dropdown-icon">▼</i>`;
            courseCardOptions.style.display = 'none'; // Hide the dropdown after selection
            confirmBtn.disabled = false; // Enable the confirm button
        });
    });

    // Redirect to selectMajor.html when the confirm button is clicked
    confirmBtn.addEventListener('click', function() {
        window.location.href = "selectMajor.html";
    });
});