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

// Placeholder function to fetch data from the database
function fetchDataFromDatabase(year, semester) {
    // TODO: Fetch the data from your database here
    return [
        { unitCode: `Placeholder-${year}-${semester}-1`, name: `Subject ${year}-${semester}-1`, semester: `${semester}`, creditPoint: "6", level: "1"},
        { unitCode: `Placeholder-${year}-${semester}-2`, name: `Subject ${year}-${semester}-2`, semester: `${semester}`, creditPoint: "6", level: "2"},
        { unitCode: `Placeholder-${year}-${semester}-3`, name: `Subject ${year}-${semester}-3`, semester: `${semester}`, creditPoint: "6", level: "3"},
        { unitCode: `Placeholder-${year}-${semester}-4`, name: `Subject ${year}-${semester}-4`, semester: `${semester}`, creditPoint: "6", level: "4"},
    ];
}

const plannerContainer = document.getElementById('plannerContainer');
const selectionContainer = document.getElementById('selectionContainer');

function createSemesterContainer(container, year, semester) {
    const data = fetchDataFromDatabase(year, semester);
    
    const semesterDiv = document.createElement('div');
    semesterDiv.className = 'semester-container';
    
    if (container === plannerContainer) {
        const header = document.createElement('div');
        header.className = 'header';
        header.textContent = `Year ${year} Sem ${semester}`;
        semesterDiv.appendChild(header);
    }

    data.forEach(subject => {
        const subjectDiv = document.createElement('div');
        subjectDiv.className = 'subject-container';

        const subjectContent = document.createElement('div');
        subjectContent.className = 'subject-content';
        subjectContent.innerHTML = `
            ${subject.unitCode}: ${subject.name}<br>
            Semester: ${subject.semester}<br>
            Credit Point: ${subject.creditPoint}<br>
            Level: ${subject.level}
        `;

        subjectDiv.appendChild(subjectContent);
        semesterDiv.appendChild(subjectDiv);
    });

    container.appendChild(semesterDiv);
}

for (let year = 1; year <= 3; year++) {
    for (let semester = 1; semester <= 2; semester++) {
        createSemesterContainer(plannerContainer, year, semester);
        if (year === 1 && semester <= 2) {
            createSemesterContainer(selectionContainer, year, semester);
        }
    }
}

// Placeholder function for saving the page as PDF
function saveAsPDF() {
    // TODO: Implement saving logic using libraries like html2canvas and jsPDF
    alert('Save as PDF functionality to be implemented.');
}

// Add event listeners to filter buttons
const filterButtons = document.querySelectorAll(".filter-button");
filterButtons.forEach(button => {
    button.addEventListener('click', function() {
        console.log(`Filter ${button.getAttribute('data-filter')} clicked`);
        // TODO: Implement the filtering logic here
    });
});
