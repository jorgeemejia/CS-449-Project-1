PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS waitlists;
CREATE TABLE waitlists (
    StudentID INTEGER,
    ClassID INTEGER,
    WaitlistDate DATE,
    PRIMARY KEY(StudentID, ClassID) 
    CONSTRAINT fk_wait_students FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    CONSTRAINT fk_wait_classes FOREIGN KEY (ClassID) REFERENCES classes(ClassID)
);
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (3, 1, '2023-09-23');
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (5, 1, '2023-10-23');
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (6, 1, '2023-10-23');
COMMIT;
