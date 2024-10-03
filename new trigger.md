DELIMITER $$

CREATE TRIGGER trg_balance_audit_after_update
AFTER UPDATE ON balance
FOR EACH ROW
BEGIN
    INSERT INTO audit_balance (
        balance_id,
        owner_id,
        plot_id,
        industry_id,
        budget_head_id,
        opening_balance,
        closing_balance,
        balance_difference,
        update_time,
        updated_by,     -- Adjust according to the user making changes (optional)
        update_reason   -- Optional: Reason for the update (if you want to log it)
    )
    VALUES (
        OLD.balance_id,                            -- The balance record being updated
        OLD.owner_id,                              -- Owner ID before the update
        OLD.plot_id,                               -- Plot ID before the update
        OLD.industry_id,                           -- Industry ID before the update
        OLD.budget_head_id,                        -- Budget Head ID before the update
        OLD.balance,                               -- Opening balance (before update)
        NEW.balance,                               -- Closing balance (after update)
        NEW.balance - OLD.balance,                 -- Difference between old and new balance
        NOW(),                                     -- Timestamp of the update
        'SYSTEM',                                  -- Assuming changes made by system or adjust to user
        'Balance update after plot allotment'      -- Optional: Specify reason for the update
    );
END$$

DELIMITER ;




CREATE TABLE audit_balance (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    balance_id INT,
    owner_id INT,
    plot_id INT,
    industry_id INT,
    budget_head_id INT,
    opening_balance DECIMAL(10,2),     -- The balance before the update
    closing_balance DECIMAL(10,2),     -- The balance after the update
    balance_difference DECIMAL(10,2),  -- Difference between old and new balance
    update_time DATETIME,              -- When the change occurred
    updated_by VARCHAR(100) DEFAULT 'SYSTEM', -- To track who made the changes
    update_reason VARCHAR(255)         -- Optional: Reason for update
);
