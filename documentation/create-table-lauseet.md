# Create Table-lauseet

```sql
CREATE TABLE role (
	id INTEGER NOT NULL, 
	name VARCHAR(80), 
	description VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);

CREATE TABLE account (
	id INTEGER NOT NULL, 
	username VARCHAR(140) NOT NULL, 
	full_name VARCHAR(140), 
	email VARCHAR(255) NOT NULL, 
	_password BLOB NOT NULL, 
	active BOOLEAN, 
	confirmed_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email), 
	CHECK (active IN (0, 1))
);

CREATE TABLE venue (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	location VARCHAR(144) NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE event (
	id INTEGER NOT NULL, 
	admin_id INTEGER NOT NULL, 
	name VARCHAR(80), 
	created_at DATETIME, 
	info TEXT, 
	venue_id INTEGER NOT NULL, 
	start_time DATETIME, 
	end_time DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(admin_id) REFERENCES account (id), 
	FOREIGN KEY(venue_id) REFERENCES venue (id)
);

CREATE TABLE roles_users (
	user_id INTEGER, 
	role_id INTEGER, 
	FOREIGN KEY(user_id) REFERENCES account (id), 
	FOREIGN KEY(role_id) REFERENCES role (id)
);

CREATE TABLE events_participants (
	user_id INTEGER NOT NULL, 
	event_id INTEGER NOT NULL, 
	PRIMARY KEY (user_id, event_id), 
	FOREIGN KEY(user_id) REFERENCES account (id), 
	FOREIGN KEY(event_id) REFERENCES event (id)
);

CREATE TABLE comment (
	id INTEGER NOT NULL, 
	event_id INTEGER NOT NULL, 
	author_id INTEGER NOT NULL, 
	post_time DATETIME, 
	comment TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(event_id) REFERENCES event (id), 
	FOREIGN KEY(author_id) REFERENCES account (id)
);
```