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
    (2, 'Jane', 'Doe', 2),
    (3, 'Michael', 'Johnson', 3);



COMMIT;
