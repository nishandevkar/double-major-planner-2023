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


    // Get references to the button and dropdown
    const selectButton = document.getElementById('selectButton');
    const dropdown = document.getElementById('dropdown');

    // Event listener for the button click
    selectButton.addEventListener('click', () => {
    // Disable the placeholder option
    document.querySelector('#dropdown option[value=""]').disabled = true;
    
    // You can add additional logic here to dynamically populate the dropdown options
    // For example, fetching options from an API, database, or predefined data.

    // For this example, we'll add a couple of options dynamically
    const newOption1 = document.createElement('option');
    newOption1.value = 'dynamicOption1';
    newOption1.textContent = 'Dynamic Option 1';
    dropdown.appendChild(newOption1);

    const newOption2 = document.createElement('option');
    newOption2.value = 'dynamicOption2';
    newOption2.textContent = 'Dynamic Option 2';
    dropdown.appendChild(newOption2);
});