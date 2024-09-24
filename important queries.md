SELECT SUM(amount) 
FROM payments
WHERE budget_head_id = (SELECT budget_head_id FROM budget_heads WHERE budget_head_name = 'Maintanance')
AND MONTH(payment_date) = MONTH(CURRENT_DATE())
AND YEAR(payment_date) = YEAR(CURRENT_DATE());

select i.ind_name,a.changed_field,a.old_value,a.new_value 
from industries_audit a
join industries i
on
i.id = a.industry_id
order 
by a.changed_at desc
limit 8;

select * from payments;



DELIMITER //

CREATE TRIGGER after_plot_allotment
AFTER INSERT ON plot_ownership
FOR EACH ROW
BEGIN
    DECLARE plotPrice DECIMAL(15, 2);
    DECLARE budget_headID int;
    

    -- Fetch the price of the plot from the 'Plots' table
    SELECT Price INTO plotPrice FROM Plots WHERE ID = NEW.plot_id;
    Select budget_head_id INTO budget_headID from budget_heads where budget_head_name = "Land Price";
        -- Insert a new balance record if one doesn't exist
        INSERT INTO balance (owner_id,plot_id,budget_head_id,balance,update_at)
        VALUES (NEW.owner_id,NEW.plot_id,budget_headID,plotPrice, NOW());
END //
DELIMITER ;
select * from ownertable;
select * from plot_ownership;
desc balance;
sle



DELIMITER $$
CREATE TRIGGER industries_update_audit
AFTER UPDATE ON industries
FOR EACH ROW
BEGIN
    -- Log changes for status
    IF OLD.ind_status <> NEW.ind_status THEN
        INSERT INTO industries_audit (industry_id, changed_field, old_value, new_value, changed_by)
        VALUES (OLD.id, 'Status', OLD.ind_status, NEW.ind_status, 'system_user'); -- Replace 'system_user' with the actual user value
    END IF;

    -- Log changes for nature
    IF OLD.ind_nature <> NEW.ind_nature THEN
        INSERT INTO industries_audit (industry_id, changed_field, old_value, new_value, changed_by)
        VALUES (OLD.id, 'Nature', OLD.ind_nature, NEW.ind_nature, 'system_user');
    END IF;

    -- Log changes for name
    IF OLD.ind_name <> NEW.ind_name THEN
        INSERT INTO industries_audit (industry_id, changed_field, old_value, new_value, changed_by)
        VALUES (OLD.id, 'Name', OLD.ind_name, NEW.ind_name, 'system_user');
    END IF;


END$$

DELIMITER ;
DROP TRIGGER IF EXISTS industries_update_audit;
select * from balance;
update balance set balance = -15000 where budget_head_id = 102;
select * from industries_audit;
select * from budget_heads;
select i.ind_name,a.changed_field,a.old_value,a.new_value from industries i join industries_audit a on i.id = a.industry_id;
alter table plots
add column price double(10,2) after area;
select * from plots;
update plots set price = 1200000;
DELIMITER $$







CREATE TRIGGER update_or_insert_balance_after_payment
AFTER INSERT ON payments
FOR EACH ROW
BEGIN
    DECLARE balance_exists INT;
    
    -- Check if the record already exists in the balance table
    SELECT COUNT(*)
    INTO balance_exists
    FROM balance
    WHERE owner_id = NEW.owner_id
    AND (plot_id = NEW.plot_id OR industry_id = NEW.industry_id)
    AND budget_head_id = NEW.budget_head_id;
    
    IF balance_exists > 0 THEN
        -- If the balance record exists, update the current_balance
        UPDATE balance
        SET balance = balance - NEW.amount
        WHERE owner_id = NEW.owner_id
        AND (plot_id = NEW.plot_id OR industry_id = NEW.industry_id)
        AND budget_head_id = NEW.budget_head_id;
        
    ELSE
        -- If the balance record does not exist, insert a new record
        INSERT INTO balance (owner_id, plot_id, industry_id, budget_head_id, balance, max_balance,update_at)
        VALUES (
            NEW.owner_id,
            NEW.plot_id,
            NEW.industry_id,
            NEW.budget_head_id,
            -NEW.amount, -- Assuming the initial balance will be the negative payment amount
            0, -- Set max_budget as needed, or manage this separately
            NOW()
        );
    END IF;
END$$

DELIMITER ;

select * from balance;

select b.budget_head_name,p.amount,p.payment_date
from payments p
join budget_heads b
on b.budget_head_id = p.budget_head_id
where p.plot_id=115;
Select * from industries;
select count(*) from plots where Land_Type = "Industrial";
Select ownname,mobile,email,address from ownertable;

update plots set land_type = "Industrial";


select i.ind_name,b.budget_head_name,p.amount
from payments p
join 
budget_heads b on
b.budget_head_id = p.budget_head_id
join industries i 
on i.id = p.industry_id
order by p.payment_date
limit 4;

update industries
set ind_name = " Mahboob Jewelry",
ind_nature = "ABC"
where id = 100;

update industries set ind_name = 'Khan', updated_at = 2024/09/18  where id = 108

 indframe = ct.CTkFrame(app,width=900,height=600,fg_color="#17202a")
    indframe.place(x=158,y=82)