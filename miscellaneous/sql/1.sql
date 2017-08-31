DROP TABLE IF EXISTS flask_user_role;
DROP TABLE IF EXISTS flask_role;
DROP TABLE IF EXISTS flask_user;
DROP TABLE IF EXISTS flask_exception;

CREATE TABLE flask_role(
	id serial PRIMARY KEY,
	name VARCHAR (100) UNIQUE NOT NULL,
	description VARCHAR (255)
);

CREATE TABLE flask_user(
	id serial PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
 	email VARCHAR(50) UNIQUE NOT NULL,
 	password VARCHAR (255) NOT NULL,
	gender CHAR(1) DEFAULT NULL CHECK (gender IN ('m', 'f')),
	title VARCHAR(40) NOT NULL,
	zipcode CHAR(5) NOT NULL,
 	created_time TIMESTAMP NOT NULL DEFAULT NOW(),
 	last_login TIMESTAMP
);

CREATE TABLE flask_user_role
(
	id serial PRIMARY KEY,
	user_id INTEGER NOT NULL,
	role_id INTEGER NOT NULL,
	grant_date TIMESTAMP NOT NULL DEFAULT NOW(),
  	UNIQUE (user_id, role_id),
  	CONSTRAINT flask_user_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES flask_role (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
  	CONSTRAINT flask_user_role_user_id_fkey FOREIGN KEY (user_id) REFERENCES flask_user (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE flask_exception
(
    id serial PRIMARY KEY,
    message TEXT,
    error TEXT,
    created_time TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO flask_role (name, description) VALUES ('authenticated', 'Default role for all registered users');
INSERT INTO flask_role (name, description) VALUES ('admin', 'Super admin role');

INSERT INTO flask_user (first_name, last_name, email, password, zipcode, title) VALUES ('Admin', 'Admin', 'admin@example.com', '$6$rounds=656000$S4GS5srTzNh9j.5t$R9q0OsFiiQK3KxDv5kKGN8mTgntmZKMbbBOZE5boubXVB2kSOSy0yGEFMT847NDN0sw/0qu0SqWh1QIq8c9um1', '20190', 'Site Admin');
INSERT INTO flask_user_role (user_id, role_id) VALUES(1, 2);