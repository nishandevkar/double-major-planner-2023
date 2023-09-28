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

    selectedCourse = ''
    // Update the button text when an option is selected
    courseOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            courseCardBtn.innerHTML = `${option.textContent} <i class="dropdown-icon">▼</i>`;
            courseCardOptions.style.display = 'none'; // Hide the dropdown after selection
            confirmBtn.disabled = false; // Enable the confirm button
            selectedCourse = `${option.textContent}`
        });
    });

    // Redirect to selectMajor.html when the confirm button is clicked
    confirmBtn.addEventListener('click', function() {
        // Create a data object to send to the Flask backend with a POST request
        const data = { 'selected_course': selectedCourse };

        // Send an AJAX POST request to the Flask route
        fetch('/submit_course', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            const queryParams = new URLSearchParams();
            queryParams.set('majors', JSON.stringify(data.majors));

            // Redirect to selectMajor.html with query parameters
            window.location.href = `/selectMajor?${queryParams.toString()}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

