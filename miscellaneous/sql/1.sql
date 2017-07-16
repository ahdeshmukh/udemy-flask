DROP TABLE IF EXISTS flask_user_role;
DROP TABLE IF EXISTS flask_role;
DROP TABLE IF EXISTS flask_user;

CREATE TABLE flask_role(
	id serial PRIMARY KEY,
	name VARCHAR (100) UNIQUE NOT NULL,
	description VARCHAR (255)
);

CREATE TABLE flask_user(
	id serial PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
 	email VARCHAR (100) UNIQUE NOT NULL,
 	password VARCHAR (255) NOT NULL,
	gender CHAR(1) DEFAULT NULL CHECK (gender IN ('m', 'f')),
	zipcode CHAR(5) NOT NULL,
 	created_on TIMESTAMP NOT NULL DEFAULT NOW(),
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


INSERT INTO flask_role (name, description) VALUES ('admin', 'Super admin role');
INSERT INTO flask_role (name, description) VALUES ('authenticated', 'Default role for all registerd users');

INSERT INTO flask_user (first_name, last_name, email, password, zipcode) VALUES ('Admin', 'Admin', 'admin@example.com', '$6$rounds=656000$S4GS5srTzNh9j.5t$R9q0OsFiiQK3KxDv5kKGN8mTgntmZKMbbBOZE5boubXVB2kSOSy0yGEFMT847NDN0sw/0qu0SqWh1QIq8c9um1', '20190')