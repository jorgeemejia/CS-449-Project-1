PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    StudentID INTEGER,
    Section INTEGER,
    PRIMARY KEY (StudentID, Section)
    CONSTRAINT fk_enroll_students FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    CONSTRAINT fk_enroll_section FOREIGN KEY (Section) REFERENCES classes(Section)
);
INSERT INTO enrollments(StudentID, Section) VALUES (1,1);
INSERT INTO enrollments(StudentID, Section) VALUES (2,1);
INSERT INTO enrollments(StudentID, Section) VALUES (3,1);
INSERT INTO enrollments(StudentID, Section) VALUES (4,1);

INSERT INTO enrollments(StudentID, Section) VALUES (5,2);
INSERT INTO enrollments(StudentID, Section) VALUES (6,2);
INSERT INTO enrollments(StudentID, Section) VALUES (7,2);
INSERT INTO enrollments(StudentID, Section) VALUES (8,2);
INSERT INTO enrollments(StudentID, Section) VALUES (9,2);


COMMIT;
