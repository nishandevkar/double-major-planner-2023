# UWA MIT CITS5206 Capstone Project
## Project Topic: Double Major Study Planner
### Team Members:
1. Dali Zheng (22850317)
2. Haoyu Li (23731411)
3. Nishan Devkar (23762917)
4. Pan Yeung Lee (23600879)
5. Yihan Liu (22696718)

### Clients:
1. Paul Lloyd UWA Curriculum Manager

**Other Stakeholders**
1. Maryam Vettoor UWA Curriculum Officer
2. CSSE Program Chairs

### Project description:
A study plan helps students to plan their sequence of units for a university course. Undergraduate courses may have two different majors. Currently, study plans are created by hand based on one or two majors or minors, each or which is defined by a unit sequence, prerequisite rules, and semester availability, which are stored in UWA's CAIDi curriculum management system. This project aims to automate the process of building a study plan for a given double major. The Double Major Study Planner software will:
1. For a given University program comprising 2 majors, automatically create a feasible study plan for students starting either in semester 1 or 2 satisfying given constraints for both majors (core units, prerequisites, semester availability).
2. Generate a visualisation of double major study plan. The visualisation could be static (eg pdf, powerpoint or html) or dynamic (eg a web application). Users should be able to visualise and edit the output.
3. Allow students or staff to propose adjustments to a study plan such as the addition or deletion of units
4. Allow students to download a completed study plan and upload an existing plan to make changes

As per: https://teaching.csse.uwa.edu.au/units/CITS5206/projects/CITS5206-Project-DoubleMajorStudyPlanner.html

### Project Estimated Time of Completion
Friday 20 October 2023 (week 12 of Semester 2 at UWA)

# Documentation

## Virtual Environment Setup & Installations

1. Download and install the latest Python version

2. Assuming you have cloned the GitHub repository to your local machine and have made it your current directory.

3. Create a virtual environment with the command-line: `python3 -m venv venv`

4. Activate virtual environment with the command-line:
   - If you are using linux/macOS, activate your virtual environment with the command-line: `source venv/bin/activate`
   - If you are using windows, activate your virtual environment with the command-line: `venv\Scripts\activate`

5. Install the required packages from the requirements.txt file with the command-line: `python3 -m pip install -r requirements.txt`

## Database

1. Download the database from Github or clone the whole Back-end braches. (commerce_database_solution1_updated.sqlite)

2. If you create your own database using SQLite

3. Replace the path './commerce_database_solution1_updated.sqlite' to your own path to your SQLite database in database.py file
   



## Secret Environment Variables

1. Create a file called `.env` in the top level directory which will be ignored by git.

2. On the first line of your `.env` file, write:
   `SQLALCHEMY_DATABASE_URI=mysql+pymysql://<username>:<password>@localhost/flaskdb`

   On the second line, add your secret key:
3. `SECRET_KEY==<your_secret_key>`

4. Remember to add the `.env` file to your `.gitignore` file to ensure it doesn’t get uploaded to your version control system. This way, every member can maintain their local configurations without affecting others.

## Run the app

1. With the repository as your current directory and your virtual environment active...

2. Launch the application using the command-line: `python3 run.py`.

3. If the webpage doesn't automatically open on your default browser, then copy the url in the terminal output into a browser window, i.e. http://127.0.0.1:5000
