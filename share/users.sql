PRAGMA foreign_key = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    UserID INTEGER PRIMARY KEY,
    UserName VARCHAR NOT NULL,
    PW VARBINARY NOT NULL
);

DROP TABLE IF EXISTS roles;
CREATE TABLE roles (
    RoleID INTEGER PRIMARY KEY,
    RoleName VARCHAR
);

DROP TABLE IF EXISTS userRole;
CREATE TABLE userRole (
    UserID INTEGER,
    RoleID INTEGER,
    PRIMARY KEY (UserID,RoleID)
    CONSTRAINT fk_users FOREIGN KEY (UserID) REFERENCES users(UserID)
    CONSTRAINT fk_roles FOREIGN KEY (RoleID) REFERENCES roles(RoleID)
);

INSERT INTO users(UserID,UserName, PW) VALUES(1,'maymarch',"pbkdf2_sha256$260000$7c345404c779c6e31691fa33d63f3f1e$nS1NifhS3b8yjFub6yRfv7wOIe7dew+tcik2StFeHs4=");

INSERT INTO roles(RoleID,RoleName) VALUES(1,'Student');
INSERT INTO roles(RoleID,RoleName) VALUES(2,'Teacher');
INSERT INTO roles(RoleID,RoleName) VALUES(3,'Regisrar');

INSERT INTO userRole(UserID,RoleID) VALUES (1,1);
INSERT INTO userRole(UserID,RoleID) VALUES (1,2);
INSERT INTO userRole(UserID,RoleID) VALUES (1,3);


COMMIT;