PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS instructors;
CREATE TABLE instructors (
    InstructorID INTEGER PRIMARY KEY,
    FirstName VARCHAR,
    LastName VARCHAR,
    UserID INTEGER,
    CONSTRAINT fk_users FOREIGN KEY (UserID) REFERENCES users(UserID)
);
INSERT INTO instructors (InstructorID, FirstName, LastName, UserID)
VALUES
    (1, 'John', 'Smith', 1),
    (2, 'Jane', 'Doe', 2),
    (3, 'Michael', 'Johnson', 3),
    (4, 'Emily', 'Wilson', 4),
    (5, 'David', 'Brown', 5),
    (6, 'Sarah', 'Anderson', 6),
    (7, 'Robert', 'Lee', 7),
    (8, 'Jennifer', 'Clark', 8),
    (9, 'William', 'Davis', 9),
    (10, 'Maria', 'Martinez', 10);



COMMIT;
