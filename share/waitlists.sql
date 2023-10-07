PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS waitlists;
CREATE TABLE waitlists (
    StudentID INTEGER,
    Section INTEGER,
    WaitlistDate DATETIME,
    PRIMARY KEY(StudentID, Section) 
    CONSTRAINT fk_wait_students FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    CONSTRAINT fk_wait_classes FOREIGN KEY (Section) REFERENCES classes(Section)
);
INSERT INTO waitlists(StudentID, Section, WaitlistDate) VALUES (10, 2, '2023-09-23 11:11:11');
INSERT INTO waitlists(StudentID, Section, WaitlistDate) VALUES (11, 2, '2023-10-23 12:12:12');
INSERT INTO waitlists(StudentID, Section, WaitlistDate) VALUES (12, 2, '2023-11-23 13:13:13');
COMMIT;
