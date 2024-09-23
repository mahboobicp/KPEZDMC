DELIMITER //

CREATE TRIGGER after_plot_allotment
AFTER INSERT ON plot_ownership
FOR EACH ROW
BEGIN
    DECLARE plotPrice DECIMAL(10, 2);

    -- Fetch the price of the plot from the 'Plots' table
    SELECT Price INTO plotPrice FROM Plots WHERE ID = NEW.plot_id;

    -- Check if the owner already has a record in the 'balance' table
    IF EXISTS (SELECT 1 FROM balance WHERE OwnerID = NEW.owner_id) THEN
        -- Update the balance, adding the plot's price
        UPDATE balance
        SET Lease_Balance = Lease_Balance + plotPrice, Last_Updated = NOW()
        WHERE OwnerID = NEW.owner_id;
    ELSE
        -- Insert a new balance record if one doesn't exist
        INSERT INTO balance (OwnerID, Lease_Balance, Last_Updated)
        VALUES (NEW.owner_id, plotPrice, NOW());
    END IF;
END //

DELIMITER ;
