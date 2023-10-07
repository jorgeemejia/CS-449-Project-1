PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS droplists;
CREATE TABLE droplists (
    StudentID INTEGER,
    Section INTEGER,
    AdminDrop BOOLEAN,
    DropDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(StudentID, Section)
    CONSTRAINT fk_drop_students FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    CONSTRAINT fk_drop_classes FOREIGN KEY (Section) REFERENCES classes(Section)
);
INSERT INTO droplists (StudentID, Section, AdminDrop, DropDate)
VALUES
    (13, 1, 0, '2023-01-15 10:30:00'),
    (14, 1, 0, '2023-01-16 14:45:00'),
    (15, 1, 1, '2023-01-17 09:15:00');
COMMIT;