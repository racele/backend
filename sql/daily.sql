-- get
select *
from daily
where date = date()
and language = ?;

-- set
insert
into daily (language, solution)
values (?, ?)
returning *;
