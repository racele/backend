-- auth
select id, password, salt
from user
where username = ?;

-- create
insert
into user (password, salt, username)
values (?, ?, ?)
returning created_at, id, username;

-- get
select created_at, id, username
from user
where id = ?;

-- search
select created_at, id, username
from user
where username like ? || '%'
order by username asc
limit 10;

-- update
update user
set password = coalesce(?, password), salt = coalesce(?, salt), username = coalesce(?, username)
where id = ?
returning created_at, id, username;
