-- pragmas
pragma foreign_keys = on;

-- daily
create table daily (
	date text not null default (date()),
	language text not null,
	solution text not null,

	unique (date, language),
	unique (language, solution)
) strict;

-- request
create table request (
	accepted_at integer,
	created_at integer not null default (unixepoch()),
	recipient_id integer not null references user,
	sender_id integer not null references user
) strict;

-- score
create table score (
	created_at integer not null default (unixepoch()),
	date text,
	guesses integer not null,
	solution text not null,
	time integer not null,
	user_id integer not null references user,

	unique (date, user_id)
) strict;

-- session
create table session (
	created_at integer not null default (unixepoch()),
	last_used_at integer not null default (unixepoch()),
	session_id integer primary key,
	token text not null unique,
	user_id integer not null references user
) strict;

-- user
create table user (
	created_at integer not null default (unixepoch()),
	password text not null,
	salt text not null,
	user_id integer primary key,
	username text not null unique collate nocase
) strict;
