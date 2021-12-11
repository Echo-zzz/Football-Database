create table people(
	ID INTEGER PRIMARY KEY AUTOINCREMENT
);


create table country(
	ctName text primary KEY
);

create table club(
	cName text PRIMARY KEY,
	nickName text,
	foundYear INTEGER,
	ctName TEXT REFERENCES country(ctName)
);

create table rounds(
	size INTEGER PRIMARY KEY,
	numberOfRounds INTEGER
);

create table event(
	eName text PRIMARY KEY,
	season text,
	cName TEXT REFERENCES club(cName)
);

create table friendly(
	eName text PRIMARY KEY REFERENCES event(eName)
);

create table tournament(
	eName text PRIMARY KEY REFERENCES event(eName)
);

create table league(
	eName text PRIMARY KEY REFERENCES event(eName),
	ctName text REFERENCES country(ctName),
	size INTEGER REFERENCES rounds(size)

);

CREATE TABLE matchTable(
	host text REFERENCES club(cName),
	visit text REFERENCES club(cName),
	matchDate INTEGER,
	eName text REFERENCES event(eName),
	awayShots INTEGER,
	homeShots INTEGER,
	awayBooks INTEGER,
	homeBooks INTEGER,
	PRIMARY KEY(host, visit, matchDate, eName)
);

create table match(
	matchID INTEGER PRIMARY KEY AUTOINCREMENT,
	matchDate INTEGER REFERENCES matchTable(matchDate),
	host text REFERENCES matchTable(host),
	visit text REFERENCES matchTable(visit),
	eName text REFERENCES event(eName)
);


create table stadium(
	sName text PRIMARY KEY,
	ctName TEXT REFERENCES country(ctName),
	capacity INTEGER,
	yearOfBuilt INTEGER
);


create table hostStadium(
	host text PRIMARY KEY REFERENCES club(cName),
	sName text REFERENCES stadium(sName)
);


create table player(
	ID INTEGER PRIMARY KEY REFERENCES people(ID),
	cName text REFERENCES club(cName),
	pName text,
	DOB INTEGER
);


create table belong(
	ID INTEGER REFERENCES people(ID),
	ctName text REFERENCES country(ctName),
	PRIMARY KEY(ID,ctName)
);

create table participate(
	cName TEXT REFERENCES club(cName),
	eName text REFERENCES event(eName),
	PRIMARY KEY(cName, eName)
);

create table attend(
	ID INTEGER REFERENCES people(ID),
	matchID INTEGER REFERENCES match(matchID),
	PRIMARY KEY(ID, matchID)
);

create table homeCourt(
	sName text REFERENCES stadium(sName),
	cName text REFERENCES club(cName),
	PRIMARY KEY(sName, cName)
);
















































