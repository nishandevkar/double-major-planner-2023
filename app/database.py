import sqlite3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

def builddb(db):

    class Major(db.Model):
        __tablename__ = 'major'
        code = db.Column(db.String(16), primary_key=True)
        title = db.Column(db.String(64))
        undergraduateDegree = db.Column(db.String(16))
        school = db.Column(db.String(64))


    db.drop_all()
    db.create_all()

    db.session.add(Major(
        code='MJD-ACCTG',
        title='Accounting',
        undergraduateDegree='BCom',
        school='UWA Business School'
    ))
    db.session.commit()

def getCourses():
    courses = ['Commerce']
    return courses

def getMajors(courses):
    majors = []
    conn = sqlite3.connect('./commerce_database_solution1.sqlite')
    cursor = conn.cursor()
    query = f"""
    SELECT major_name
    FROM major_table
    WHERE major_name!='Foundation'
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        majors.append(row[0])
    return majors

def process_duplicates(raw_data):
    processed_data = []
    seen_units = {}

    for unit in raw_data:
        unit_code, unit_name = unit[0], unit[1]
        
        if (unit_code, unit_name) in seen_units:
            prev_unit = seen_units[(unit_code, unit_name)]
            
            if unit[2:] == prev_unit[2:]:
                continue
            else:
                merged_unit = (
                    unit_code, 
                    unit_name, 
                    unit[2],
                    unit[3],
                    unit[4],
                    unit[5],
                    str(unit[6] == 'true' or prev_unit[6] == 'true').lower(),
                    str(unit[7] == 'true' or prev_unit[7] == 'true').lower()
                )
                seen_units[(unit_code, unit_name)] = merged_unit
        else:
            seen_units[(unit_code, unit_name)] = unit
    
    processed_data = list(seen_units.values())
    return processed_data

def process_units(data):
    print(f"Input data: {data}")  
    
    # Check the length of a sample unit
    print(f"Sample unit: {data[0]}")  
    print(f"Length of sample unit: {len(data[0])}")  
    
    foundation_core_units = sorted(
        [unit for unit in data if unit[5] == 1 or unit[3] == "Foundation"],
        key=lambda x: x[2]  
    )

    print(f"Foundation and core units: {foundation_core_units}")  
    
    organized_units = {
        "1st year Sem1": [],
        "1st year Sem2": [],
        "2nd year Sem1": [],
        "2nd year Sem2": [],
        "3rd year Sem1": [],
        "3rd year Sem2": []
    }
    
    # Check if we have enough data to check sem1 and sem2 availability
    try:
        for unit in foundation_core_units:
            for sem_level in organized_units.keys():
                # Check the unit should be placed in this sem and level, and check if the row already has 4 units
                if (("Sem1" in sem_level and unit[6] == 'true') or 
                    ("Sem2" in sem_level and unit[7] == 'true')) and len(organized_units[sem_level]) < 4:
                    organized_units[sem_level].append(unit)
                    break  

    except IndexError as e:
        print(f"IndexError for unit {unit}: {e}")
    
    print(f"Organized units: {organized_units}")  
    return organized_units


def getUnits(selected_majors):
    conn = sqlite3.connect('./commerce_database_solution1.sqlite')
    cursor = conn.cursor()
    query = """
    SELECT 
    unit_table.Code, 
    unit_table.Title, 
    unit_table.Level,  -- 修改这里
    unit_with_major.major_name, 
    unit_table.prerequisites, 
    unit_table.Is_Core,
    CASE 
        WHEN '1 Semester 2023' IN (Avail_1_Semester_Year, Avail_2_Semester_Year, Avail_3_Semester_Year, Avail_4_Semester_Year, Avail_5_Semester_Year, Avail_6_Semester_Year, Avail_7_Semester_Year) 
            THEN 'true'
        ELSE 'false'
    END AS sem1,
    CASE 
        WHEN '2 Semester 2023' IN (Avail_1_Semester_Year, Avail_2_Semester_Year, Avail_3_Semester_Year, Avail_4_Semester_Year, Avail_5_Semester_Year, Avail_6_Semester_Year, Avail_7_Semester_Year) 
            THEN 'true'
        ELSE 'false'
    END AS sem2
FROM 
    unit_table, unit_with_major, unit_with_level
WHERE
    (unit_with_major.major_name=? OR unit_with_major.major_name=? OR unit_with_major.major_name='Foundation') AND
    unit_table.Code=unit_with_major.Code AND unit_table.Code=unit_with_level.Code AND
    unit_table.major=unit_with_major.major_id AND
    ('1 Semester 2023' IN (Avail_1_Semester_Year, Avail_2_Semester_Year, Avail_3_Semester_Year, Avail_4_Semester_Year, Avail_5_Semester_Year, Avail_6_Semester_Year, Avail_7_Semester_Year) OR 
    '2 Semester 2023' IN (Avail_1_Semester_Year, Avail_2_Semester_Year, Avail_3_Semester_Year, Avail_4_Semester_Year, Avail_5_Semester_Year, Avail_6_Semester_Year, Avail_7_Semester_Year));
    """
    cursor.execute(query, (selected_majors[0], selected_majors[1]))
    raw_data = cursor.fetchall()
    print(f"Raw Data: {raw_data}")
    
    # Process the data to remove/merge duplicates
    processed_data = process_duplicates(raw_data)
    print(f"Processed Data: {processed_data}")
    
    query = """
        SELECT *
        FROM major_table
        WHERE major_table.major_name=? OR major_table.major_name=?
    """
    cursor.execute(query, (selected_majors[0], selected_majors[1]))
    structures = cursor.fetchall()
    conn.close()
    return processed_data, structures

def ifvalid(db, majors, units):
    flag = True
    ## TODO: Check if the units selection is valid.

    ##
    return flag

