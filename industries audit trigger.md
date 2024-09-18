DELIMITER $$

CREATE TRIGGER industries_update_audit
AFTER UPDATE ON industries
FOR EACH ROW
BEGIN
    -- Log changes for status
    IF OLD.status <> NEW.status THEN
        INSERT INTO industries_audit (industry_id, changed_field, old_value, new_value, changed_by)
        VALUES (OLD.industry_id, 'status', OLD.status, NEW.status, 'system_user'); -- Replace 'system_user' with the actual user value
    END IF;

    -- Log changes for nature
    IF OLD.nature <> NEW.nature THEN
        INSERT INTO industries_audit (industry_id, changed_field, old_value, new_value, changed_by)
        VALUES (OLD.industry_id, 'nature', OLD.nature, NEW.nature, 'system_user');
    END IF;

    -- Log changes for name
    IF OLD.name <> NEW.name THEN
        INSERT INTO industries_audit (industry_id, changed_field, old_value, new_value, changed_by)
        VALUES (OLD.industry_id, 'name', OLD.name, NEW.name, 'system_user');
    END IF;

    -- Log changes for director
    IF OLD.director <> NEW.director THEN
        INSERT INTO industries_audit (industry_id, changed_field, old_value, new_value, changed_by)
        VALUES (OLD.industry_id, 'director', OLD.director, NEW.director, 'system_user');
    END IF;

END$$

DELIMITER ;


### Actual Trigger
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