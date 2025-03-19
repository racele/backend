-- accept
update request
set accepted_at = coalesce(accepted_at, unixepoch())
where recipient_id = ?
and sender_id = ?
returning *;

-- accepted
select *
from request
where accepted_at is not null
and ? in (recipient_id, sender_id)
order by accepted_at desc;

-- create
insert
into request (recipient_id, sender_id)
values (?, ?)
returning *;

-- delete
delete
from request
where (?, ?) in ((recipient_id, sender_id), (sender_id, recipient_id));

-- exists
select count(*)
from request
where (?, ?) in ((recipient_id, sender_id), (sender_id, recipient_id));

-- received
select *
from request
where accepted_at is null
and recipient_id = ?
order by created_at desc;

-- sent
select *
from request
where accepted_at is null
and sender_id = ?
order by created_at desc;
