-- create
insert into token (token, user)
values (?, ?);

-- resolve
select user
from token
where token = ?;
