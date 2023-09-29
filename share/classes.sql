PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
    ClassID INTEGER PRIMARY KEY,
    ClassSectionNumber INTEGER, 
    CourseID INTEGER,
    DepartmentID INTEGER,
    InstructorID INTEGER,
    ClassCurrentEnrollment INTEGER,
    ClassMaximumEnrollment INTEGER,
    CONSTRAINT fk_courses
    FOREIGN KEY (CourseID) REFERENCES courses(CourseID)
    CONSTRAINT fk_departments
    FOREIGN KEY (DepartmentID) REFERENCES departments(DepartmentID)
    CONSTRAINT fk_instructors
    FOREIGN KEY (InstructorID) REFERENCES instructors(InstructorID) 
);
INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, DepartmentID, InstructorID, ClassCurrentEnrollment, ClassMaximumEnrollment) 
             VALUES(01,01,01,01,01,01,05);
COMMIT;