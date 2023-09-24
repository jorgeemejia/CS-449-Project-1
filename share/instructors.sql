PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS instructors;
CREATE TABLE instructors (
    InstructorID INTEGER PRIMARY KEY,
    FirstName VARCHAR,
    LastName VARCHAR
);
INSERT INTO instructors(InstructorID, FirstName, LastName) VALUES(01, 'John', 'Smith');
INSERT INTO instructors(InstructorID, FirstName, LastName) VALUES(02, 'Kenytt', 'Avery');
INSERT INTO instructors(InstructorID, FirstName, LastName) VALUES(03, 'Paul', 'Wall');

COMMIT;
