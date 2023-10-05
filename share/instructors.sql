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
INSERT INTO instructors(InstructorID, FirstName, LastName, UserID) VALUES(01, 'John', 'Smith', 1);
INSERT INTO instructors(InstructorID, FirstName, LastName, UserID) VALUES(02, 'Kenytt', 'Avery', 2);
INSERT INTO instructors(InstructorID, FirstName, LastName, UserID) VALUES(03, 'Paul', 'Wall', 3);
INSERT INTO instructors(InstructorID, FirstName, LastName, UserID) VALUES(04, 'Chris', 'Carpenter', 4);
INSERT INTO instructors(InstructorID, FirstName, LastName, UserID) VALUES(05, 'Jack', 'White', 5);


COMMIT;
