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
    (1, 'Michael', 'Johnson', 4),
    (2, 'Emily', 'Wilson', 5),
    (3, 'David', 'Brown', 6),
    (4, 'Sarah', 'Anderson', 7),
    (5, 'Robert', 'Lee', 8),
    (6, 'Jennifer', 'Clark', 9),
    (7, 'William', 'Davis', 10),
    (8, 'Maria', 'Martinez', 11),
    (9, 'Linda', 'Garcia', 12),
    (10, 'James', 'Hernandez', 13),
    (11, 'Sophia', 'Williams', 14),
    (12, 'Ethan', 'Jones', 15),
    (13, 'Olivia', 'Brown', 16),
    (14, 'Liam', 'Davis', 17),
    (15, 'Ava', 'Garcia', 18),
    (16, 'Joe', 'Markez', 19),
    (17, 'Luis', 'Silver', 20);



COMMIT;