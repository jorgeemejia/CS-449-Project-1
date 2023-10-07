BEGIN TRANSACTION;
DROP TABLE IF EXISTS settings;
CREATE TABLE settings (
    SettingID INTEGER PRIMARY KEY,
    SettingName TEXT NOT NULL,
    SettingValue TEXT NOT NULL
);

INSERT INTO settings (SettingName, SettingValue) 
VALUES 
    ('auto_enrollment_status', 'enabled');

COMMIT;