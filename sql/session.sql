-- clear
delete
from session
where token <> ?
and user_id = ?;

-- create
insert
into session (token, user_id)
values (?, ?);

-- delete
delete
from session
where session_id = ?
and user_id = ?;

-- list
select created_at, last_used_at, session_id, user_id
from session
where user_id = ?
order by last_used_at desc;

-- resolve
update session
set last_used_at = unixepoch()
where token = ?
returning token, user_id;
