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
    (1, 1, 1, 1, 30),
    (2, 2, 2, 2, 25),
    (3, 3, 3, 3, 20),
    (4, 1, 4, 4, 35),
    (5, 2, 5, 5, 28),
    (6, 3, 6, 6, 32),
    (7, 1, 7, 7, 22),
    (8, 2, 8, 8, 18),
    (9, 3, 9, 9, 27),
    (10, 1, 10, 10, 23);


COMMIT;