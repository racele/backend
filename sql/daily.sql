-- get
select *
from daily
where created_at = date()
and language = ?;

-- set
insert
into daily (language, solution)
values (?, ?)
returning *;
