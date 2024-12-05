-- pragmas
pragma foreign_keys = on;

-- request
create table request (
	accepted text,
	recipient integer not null references user,
	requested text not null default current_timestamp,
	sender integer not null references user,
	check (recipient <> sender)
) strict;

-- token
create table token (
	token text not null unique,
	user integer not null references user
) strict;

-- user
create table user (
	id integer primary key,
	password text not null,
	salt text not null,
	username text not null unique
) strict;
