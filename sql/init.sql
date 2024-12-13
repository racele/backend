-- pragmas
pragma foreign_keys = on;

-- request
create table request (
	accepted_at integer,
	created_at integer not null default (unixepoch()),
	recipient_id integer not null references user,
	sender_id integer not null references user
) strict;

-- session
create table session (
	created_at integer not null default (unixepoch()),
	last_used_at integer,
	token text not null unique,
	user_id integer not null references user
) strict;

-- user
create table user (
	created_at integer not null default (unixepoch()),
	id integer primary key,
	password text not null,
	salt text not null,
	username text not null unique collate nocase
) strict;
