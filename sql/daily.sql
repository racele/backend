-- get
select *
from daily
where created_at = date();

-- set
insert
into daily (solution)
values (?)
returning *;
