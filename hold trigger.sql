--LINK: https://www.postgresql.org/docs/current/plpgsql-statements.html#PLPGSQL-STATEMENTS-DIAGNOSTICS
--DESCRIPTION: Using found in function for select into

CREATE OR REPLACE FUNCTION book_returned()
RETURNS TRIGGER AS $$
DECLARE 
	reserved_user INTEGER
	reserved_hold INTEGER
BEGIN
	IF OLD.return_date IS NULL AND NEW.return_date IS NOT NULL THEN
		SELECT user_id, hold_id
		INTO reserved_user, reserved_hold
		FROM holds
		WHERE holds.book_id = NEW.book_id AND holds.hold_date = (SELECT MIN(hold_date)
																  FROM holds
																  WHERE holds.book_id = NEW.book_id)
		LIMIT 1;

		IF NOT FOUND THEN
			UPDATE copies
			SET is_available = TRUE
			WHERE copies.copy_id = NEW.copy_id;
		ELSE
			INSERT INTO reservations(copy_id, user_id, checkout_date, due_date)
			VALUES
				(NEW.copy_id, reserved_user, CURRENT_DATE, CURRENT_DATE + 7);

			UPDATE copies
			SET is_available = FALSE
			WHERE copies.copy_id = NEW.copy_id;

			DELETE FROM holds
			WHERE holds.hold_id = reserved_hold
		END IF;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER book_returned
BEFORE UPDATE ON reservations
FOR EACH ROW
EXECUTE FUNCTION book_returned();