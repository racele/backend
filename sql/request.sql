-- accept
update request
set accepted = current_timestamp
where accepted is null
and recipient = ?
and sender = ?;

-- create
insert into request (recipient, sender)
values (?, ?);

-- decline
delete from request
where accepted is null
and recipient = ?
and sender = ?;

-- exists
select count(*)
from request
where (?, ?) in ((recipient, sender), (sender, recipient))
limit 1;
