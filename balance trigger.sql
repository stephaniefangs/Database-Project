CREATE OR REPLACE FUNCTION balance_updated()
RETURNS TRIGGER AS $$
BEGIN
	IF OLD.outstanding_balance <> NEW.outstanding_balance THEN
		INSERT INTO balance_history(amount, date_of_change, user_id)
        VALUES
            (NEW.outstanding_balance - OLD.outstanding_balance, NOW(), OLD.user_id);
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER balance_updated
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION balance_updated();