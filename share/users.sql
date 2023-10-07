PRAGMA foreign_key = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    UserID INTEGER PRIMARY KEY,
    Role TEXT CHECK (Role IN ('Student', 'Instructor', 'Registrar'))
);
INSERT INTO users (UserID, Role)
VALUES
    (1, 'Registrar'),
    (2, 'Instructor'),
    (3, 'Instructor'),
    (4, 'Student'),
    (5, 'Student'),
    (6, 'Student'),
    (7, 'Student'),
    (8, 'Student'),
    (9, 'Student'),
    (10, 'Student'),
    (11, 'Student'),
    (12, 'Student'),
    (13, 'Student'),
    (14, 'Student'),
    (15, 'Student'),
    (16, 'Student'),
    (17, 'Student'),
    (18, 'Student'),
    (19, 'Student'),
    (20, 'Student');
COMMIT;