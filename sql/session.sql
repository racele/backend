-- clear
delete
from session
where token <> ?
and user_id = ?;

-- create
insert
into session (token, user_id)
values (?, ?);

-- resolve
update session
set last_used_at = unixepoch()
where token = ?
returning user_id;
