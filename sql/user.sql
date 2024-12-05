-- create
insert into user (password, salt, username)
values (?, ?, ?);

-- get
select *
from user
where username = ?;

-- rename
update user
set username = ?
where id = ?;
