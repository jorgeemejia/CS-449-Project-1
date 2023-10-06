PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS droplists;
CREATE TABLE droplists (
    StudentID INTEGER,
    ClassID INTEGER,
    AdminDrop BOOLEAN,
    DropDate DATETIME,
    PRIMARY KEY(StudentID, ClassID)
    CONSTRAINT fk_drop_students FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    CONSTRAINT fk_drop_classes FOREIGN KEY (ClassID) REFERENCES classes(ClassID)
);
INSERT INTO droplists (StudentID, ClassID, AdminDrop, DropDate)
VALUES
    (11, 1, 0, '2023-01-15 10:30:00'),
    (12, 2, 0, '2023-01-16 14:45:00'),
    (13, 3, 1, '2023-01-17 09:15:00'),
    (14, 4, 0, '2023-01-18 16:20:00'),
    (15, 5, 1, '2023-01-19 11:55:00');
