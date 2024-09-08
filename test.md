## Join Query


select p.plot_number,p.zone,p.Area,o.CNIC,o.ownname,o.Mobile,po.start_date
from plots p
join
plot_ownership po
on p.id = po.plot_id
join
ownertable o
on o.id = po.owner_id;

# Search query for payments details in different budget heads

select o.ownname,i.ind_name,b.budget_head_name,p.amount
from payments p
join ownertable o 
on o.id = p.owner_id
join industries i
on i.id = p.industry_id
join budget_heads b
on b.budget_head_id = p.budget_head_id;

## Search query for tree
select p.plot_number,p.zone,p.Area,o.ownname,o.Mobile,i.ind_name,i.ind_nature,p.id,o.id
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


f"select p.plot_number,p.zone,p.Area,o.CNIC,o.ownname,o.Mobile,po.start_date from plots p join plot_ownership po on p.id = po.plot_id join ownertable o on o.id = po.owner_id where {cond} like {value};"

select p.plot_number,p.zone,p.Area,o.ownname,o.Mobile,i.ind_name,i.ind_nature from plots p join plot_ownership po on p.id = po plot_id join ownertable o on o.id = po.owner_id left join industries i on i.id = p.id where {cond} like {value};


cur,con = database_connect()
    query = f"select budget_head_id from budget_heads where budget_head_name = '{head}';"
    cur.execute(query)
    result = cur.fetchone()
    print(query)
    print(result)
    if result is None:
        cur.execute("SELECT budget_head_id FROM budget_heads ORDER BY budget_head_id DESC LIMIT 1")
        fetch_id = cur.fetchone() 
        if fetch_id is None:
        # If there's no row or id is NULL, insert the specific value (e.g., 1)
            budget_head_id = 100
        else:
        # If id is not NULL, get the last id and increment the value by 1
            last_id = result[0]
            budget_head_id = last_id + 1
   
        #query = "insert into budget_heads(budget_head_id,budget_head_name) VALUES(%s,%s)"
        insert_query = """INSERT INTO budget_heads (budget_head_id,budget_head_name) 
                                    VALUES (%s,%s)"""
        data = (budget_head_id,head)
        cur.execute(insert_query,data)
        con.commit()
        print(head)
        return budget_head_id
    else:
        return result[0]