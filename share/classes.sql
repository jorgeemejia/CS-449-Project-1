PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
    Section INTEGER PRIMARY KEY,
    CourseID INTEGER,
    InstructorID INTEGER,
    ClassMaximumEnrollment INTEGER,
    CONSTRAINT fk_courses FOREIGN KEY (CourseID) REFERENCES courses(CourseID)
    CONSTRAINT fk_instructors FOREIGN KEY (InstructorID) REFERENCES instructors(InstructorID) 
);
INSERT INTO classes (Section, CourseID, InstructorID, ClassMaximumEnrollment)
VALUES
    (1, 1, 1, 5),
    (2, 1, 2, 5);


COMMIT;