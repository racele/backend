-- access
select password, salt, user_id
from user
where username = ?;

-- create
insert
into user (password, salt, username)
values (?, ?, ?)
returning created_at, user_id, username;

-- get
select created_at, user_id, username
from user
where user_id = ?;

-- search
select created_at, user_id, username
from user
where username like ? || '%'
order by username asc
limit 10;

-- update
update user
set password = coalesce(?, password), salt = coalesce(?, salt), username = coalesce(?, username)
where user_id = ?
returning created_at, user_id, username;
