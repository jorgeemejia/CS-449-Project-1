PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    StudentID INTEGER PRIMARY KEY,
    FirstName VARCHAR,
    LastName VARCHAR,
    UserID INTEGER,
    CONSTRAINT fk_student_users FOREIGN KEY (UserID) REFERENCES users(UserID)
);
INSERT INTO students (StudentID, FirstName, LastName, UserID)
VALUES
    (1, 'Michael', 'Johnson', 6),
    (2, 'Emily', 'Wilson', 7),
    (3, 'David', 'Brown', 8),
    (4, 'Sarah', 'Anderson', 9),
    (5, 'Robert', 'Lee', 10),
    (6, 'Jennifer', 'Clark', 11),
    (7, 'William', 'Davis', 12),
    (8, 'Maria', 'Martinez', 13),
    (9, 'Linda', 'Garcia', 14),
    (10, 'James', 'Hernandez', 15),
    (11, 'Sophia', 'Williams', 16),
    (12, 'Ethan', 'Jones', 17),
    (13, 'Olivia', 'Brown', 18),
    (14, 'Liam', 'Davis', 19),
    (15, 'Ava', 'Garcia', 20);



COMMIT;