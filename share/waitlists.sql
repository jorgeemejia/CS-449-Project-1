PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS waitlists;
CREATE TABLE waitlists (
    StudentID INTEGER,
    ClassID INTEGER,
    WaitlistDate DATETIME,
    PRIMARY KEY(StudentID, ClassID) 
    CONSTRAINT fk_wait_students FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    CONSTRAINT fk_wait_classes FOREIGN KEY (ClassID) REFERENCES classes(ClassID)
);
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (3, 1, '2023-09-23 11:11:11');
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (5, 1, '2023-10-23 12:12:12');
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (6, 1, '2023-11-23 13:13:13');
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (7, 1, '2023-12-23 14:14:14');
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (6, 2, '2023-10-23 15:15:15');
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (4, 3, '2023-10-23 16:16:16');
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (3, 2, '2023-10-23 17:17:17');
INSERT INTO waitlists(StudentID, ClassID, WaitlistDate) VALUES (1, 1, '2023-13-23 18:18:18');


COMMIT;
