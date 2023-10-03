PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
    ClassID INTEGER PRIMARY KEY,
    ClassSectionNumber INTEGER, 
    CourseID INTEGER,
    InstructorID INTEGER,
    ClassMaximumEnrollment INTEGER,
    CONSTRAINT fk_courses FOREIGN KEY (CourseID) REFERENCES courses(CourseID)
    CONSTRAINT fk_instructors FOREIGN KEY (InstructorID) REFERENCES instructors(InstructorID) 
);


INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment) 
             VALUES(1,1,1,1,10);
INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment) 
             VALUES(2,2,1,1,10);
INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment) 
             VALUES(3,2,2,2,10);
INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment) 
             VALUES(4,1,3,3,10);
INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment) 
             VALUES(5,1,4,4,10);
INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment) 
             VALUES(6,1,4,4,10);   
INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment) 
             VALUES(7,1,5,5,10);      

COMMIT;