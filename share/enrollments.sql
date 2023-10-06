PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    StudentID INTEGER,
    ClassID INTEGER,
    PRIMARY KEY (StudentID, ClassID)
    CONSTRAINT fk_enroll_students FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    CONSTRAINT fk_enroll_classes FOREIGN KEY (ClassID) REFERENCES classes(ClassID)
);
INSERT INTO enrollments(StudentID, ClassID) VALUES (1,1);
INSERT INTO enrollments(StudentID, ClassID) VALUES (2,2);
INSERT INTO enrollments(StudentID, ClassID) VALUES (3,3);
INSERT INTO enrollments(StudentID, ClassID) VALUES (4,4);
INSERT INTO enrollments(StudentID, ClassID) VALUES (5,5);


COMMIT;
