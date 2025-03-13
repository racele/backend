-- create
insert
into score (date, guesses, solution, time, user_id)
values (?, ?, ?, ?, ?)
returning *;

-- daily
select *
from score
where date is not null
and user_id = ?
order by time asc;

-- practice
select *
from score
where date is null
and user_id = ?
order by time asc;
