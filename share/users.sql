PRAGMA foreign_key = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    UserID INTEGER PRIMARY KEY
    Role TEXT CHECK (ROLE IN ('Student', 'Instructor', 'Registrar'))
);
INSERT INTO users (UserID, Role) VALUES(1,'Instructor')
INSERT INTO users (UserID, Role) VALUES(2,'Instructor')
INSERT INTO users (UserID, Role) VALUES(3,'Instructor')
INSERT INTO users (UserID, Role) VALUES(4,'Instructor')
INSERT INTO users (UserID, Role) VALUES(5,'Instructor')
INSERT INTO users (UserID, Role) VALUES(6,'Student')
INSERT INTO users (UserID, Role) VALUES(7,'Student')
INSERT INTO users (UserID, Role) VALUES(8,'Student')
INSERT INTO users (UserID, Role) VALUES(9,'Student')
INSERT INTO users (UserID, Role) VALUES(10,'Student')
INSERT INTO users (UserID, Role) VALUES(11,'Student')
INSERT INTO users (UserID, Role) VALUES(12,'Student')
INSERT INTO users (UserID, Role) VALUES(13,'Student')
INSERT INTO users (UserID, Role) VALUES(14,'Student')
INSERT INTO users (UserID, Role) VALUES(15,'Student')


COMMIT;