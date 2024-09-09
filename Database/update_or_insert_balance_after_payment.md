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
