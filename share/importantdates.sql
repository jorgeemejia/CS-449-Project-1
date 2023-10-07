PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS importantdates;
CREATE TABLE importantdates (
    EventID INTEGER PRIMARY KEY,
    EventName TEXT NOT NULL,
    EventDate DATE NOT NULL
);

INSERT INTO importantdates (EventName, EventDate) 
VALUES 
    ('last_day_to_enroll', '2023-09-05');
COMMIT;