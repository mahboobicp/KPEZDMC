## Join Query


select p.plot_number,p.zone,p.Area,o.CNIC,o.ownname,o.Mobile,po.start_date
from plots p
join
plot_ownership po
on p.id = po.plot_id
join
ownertable o
on o.id = po.owner_id;



## Search query for tree
select p.plot_number,p.zone,p.Area,o.ownname,o.Mobile,i.ind_name,i.ind_nature
from plots p
join
plot_ownership po
on p.id = po.plot_id
join
ownertable o
on o.id = po.owner_id
left join
industries i
on i.id = p.id;
