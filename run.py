from app import app
import sqlite3

app.run(debug=True)

def fetch_data_from_unit():

    conn = sqlite3.connect('./majors_database.db')

    cursor = conn.cursor()
    

    cursor.execute('SELECT * FROM Unit')
    
    rows = cursor.fetchall()
    
 
    conn.close()
    
    return rows

if __name__ == '__main__':
    app.run()
