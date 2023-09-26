import sqlite3
from flask import Flask


def fetch_data_from_unit():

    conn = sqlite3.connect('/Users/panyeunglee/Documents/project capstone/double-major-planner-2023/basic_html/majors_database.db')

    cursor = conn.cursor()
    

    cursor.execute('SELECT * FROM MAJOR')
    

    rows = cursor.fetchall()
    
 
    conn.close()
    
    return rows

if __name__ == "__main__":
    data = fetch_data_from_unit()
    for row in data:
        print(row)
