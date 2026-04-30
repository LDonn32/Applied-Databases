-- schema.sql
CREATE DATABASE IF NOT EXISTS conference_management;
USE conference_management;

-- Company table
CREATE TABLE IF NOT EXISTS company (
    companyID INT AUTO_INCREMENT PRIMARY KEY,
    companyName VARCHAR(100) NOT NULL
);

-- Speaker table
CREATE TABLE IF NOT EXISTS speaker (
    speakerID INT AUTO_INCREMENT PRIMARY KEY,
    speakerName VARCHAR(100) NOT NULL
);

-- Room table
CREATE TABLE IF NOT EXISTS room (
    roomID INT AUTO_INCREMENT PRIMARY KEY,
    roomName VARCHAR(100) NOT NULL
);

-- Session table
CREATE TABLE IF NOT EXISTS session (
    sessionID INT AUTO_INCREMENT PRIMARY KEY,
    sessionTitle VARCHAR(200) NOT NULL,
    speakerID INT,
    roomID INT,
    FOREIGN KEY (speakerID) REFERENCES speaker(speakerID),
    FOREIGN KEY (roomID) REFERENCES room(roomID)
);

-- Attendee table
CREATE TABLE IF NOT EXISTS attendee (
    attendeeID INT AUTO_INCREMENT PRIMARY KEY,
    attendeeName VARCHAR(100) NOT NULL,
    dateOfBirth DATE NOT NULL,
    email VARCHAR(150),
    jobTitle VARCHAR(100),
    companyID INT,
    FOREIGN KEY (companyID) REFERENCES company(companyID)
);

-- Attendee-Session junction table
CREATE TABLE IF NOT EXISTS attendee_session (
    attendeeID INT,
    sessionID INT,
    PRIMARY KEY (attendeeID, sessionID),
    FOREIGN KEY (attendeeID) REFERENCES attendee(attendeeID),
    FOREIGN KEY (sessionID) REFERENCES session(sessionID)
);
