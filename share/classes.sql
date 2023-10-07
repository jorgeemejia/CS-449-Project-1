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
INSERT INTO classes (ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment)
VALUES
    (1, 1, 1, 1, 5),
    (2, 2, 1, 2, 5);


COMMIT;