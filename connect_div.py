from flask import Flask, jsonify, send_from_directory, render_template
import sqlite3


app = Flask(__name__)

def fetch_data_from_unit():
    conn = sqlite3.connect('/Users/panyeunglee/Documents/project capstone/double-major-planner-2023/basic_html/majors_database.db') 
    cursor = conn.cursor()
    
    query = f"""
    SELECT Code, Title, level, credit 
    FROM Unit 
    WHERE Avail_1_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
          Avail_2_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
          Avail_3_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
          Avail_4_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
          Avail_5_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
          Avail_6_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
          Avail_7_Semester_Year IN ('1 Semester 2023', '2 Semester 2023')
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/fetchUnits')
def fetch_units_route():
    data = fetch_data_from_unit()  
    return jsonify(data)

@app.route('/page4')
def serve_page4():
    return render_template('page4.html')

@app.route('/test')
def serve_test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)