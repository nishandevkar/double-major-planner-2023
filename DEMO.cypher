// CREATE DEMO
CREATE (:Student {id: 'ID1234'})


CREATE (:Course {code: 'BACT'})


CREATE (:Subject {code: 'mgmt1001', level: 'LV1'})
CREATE (:Subject {code: 'mgmt1002', level: 'LV1'})



CREATE (:Semester {name: 'sem1', year: 2023, mode: 'Face to face'})
CREATE (:Semester {name: 'sem2', year: 2023, mode: 'Online'})
WITH*
MATCH (student:Student {id: 'ID1234'}), (course:Course {code: 'BACT'})
CREATE (student)-[:STUDY_IN]->(course)
WITH*
MATCH (course:Course {code: 'BACT'}), (coreSubject:Subject {code: 'mgmt1001'})
CREATE (course)-[:MAJOR]->(coreSubject)
WITH*
MATCH (course:Course {code: 'BACT'}), (electiveSubject:Subject {code: 'mgmt1002'})
CREATE (course)-[:ELECTIVE]->(electiveSubject)
WITH*
MATCH (subject:Subject {code: 'mgmt1001'}), (semester1:Semester {name: 'sem1', year: 2023, mode: 'Face to face'}), (semester2:Semester {name: 'sem2', year: 2023, mode: 'Online'})
CREATE (subject)-[:OFFERED_IN]->(semester1)
CREATE (subject)-[:OFFERED_IN]->(semester2)
WITH*
MATCH (subject:Subject {code: 'mgmt1002'}), (semester1:Semester {name: 'sem1', year: 2023, mode: 'Face to face'})
CREATE (subject)-[:OFFERED_IN]->(semester1)

//ADD DEMO
CREATE (:Course {code: 'BBUS'})


CREATE (:Subject {code: 'MBUS2001'})
CREATE (:Subject {code: 'MBUS2002'})


CREATE (:Semester {name: 'sem2', year: 2023, mode: 'Online'})
WITH*
MATCH (course:Course {code: 'BBUS'}), (subject1:Subject {code: 'MBUS2001'}), (subject2:Subject {code: 'MBUS2002'}), (semester:Semester {name: 'sem2', year: 2023, mode: 'Online'})
CREATE (course)-[:MAJOR]->(subject1)
CREATE (course)-[:ELECTIVE]->(subject2)
CREATE (subject1)-[:OFFERED_IN]->(semester)
CREATE (subject2)-[:OFFERED_IN]->(semester)

//RELATIONSHIP DEMO
MATCH (student:Student {id: 'ID1234'}), (course:Course {code: 'BBUS'})
CREATE (student)-[:STUDY_IN]->(course)


//SEARCH DEMO
MATCH (student:Student {id: 'ID1234'})-[:STUDY_IN]->(course)-[:MAJOR]->(subject)-[:OFFERED_IN]->(semester:Semester {name: 'sem2'})
RETURN subject

MATCH (student:Student {id: 'ID1234'})-[:STUDY_IN]->(course)-[:MAJOR]->(subject:Subject {level: 'LV1'})-[:OFFERED_IN]->(semester:Semester {name: 'sem2'})
RETURN subject

//PREREQUISITE DEMO
MATCH (subject1:Subject {code: 'MBUS2001'}), (subject2:Subject {code: 'MBUS2002'})
CREATE (subject1)-[:PREREQUISITE]->(subject2)

//NO PREREQUISITE DEMO 
MATCH (student:Student {id: 'ID1234'})-[:STUDY_IN]->(course)-[:MAJOR]->(subject:Subject {code: 'MBUS2002'})-[:PREREQUISITE]->(prerequisite)
WHERE NOT (student)-[:COMPLETED]->(prerequisite)
RETURN subject, prerequisite