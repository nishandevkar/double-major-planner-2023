from app import app
import sqlite3
import os



app.run(debug=True)

def fetch_data_from_unit():

    conn = sqlite3.connect('./majors_database.db')

    cursor = conn.cursor()
    

    cursor.execute('SELECT * FROM Unit')
    
    rows = cursor.fetchall()
    
 
    conn.close()
    
    return rows


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)  # Use 5000 as a default port if PORT is not set
    app.run(host='0.0.0.0', port=port)
