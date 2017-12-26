DELIMITER //
CREATE TRIGGER verify_date
BEFORE INSERT ON api_flight 
FOR EACH ROW
BEGIN
	CALL validate_flight_datetime(NEW.arrival_time);
    IF NOT (@valid)
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Incorrect arrival time';
    END IF;
    
	CALL validate_flight_datetime(NEW.departure_time);
    IF NOT (@valid)
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Incorrect departure time';
    END IF;
END //

DELIMITER ;