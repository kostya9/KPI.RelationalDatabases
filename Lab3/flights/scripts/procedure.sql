DELIMITER //
CREATE PROCEDURE validate_flight_datetime(IN flight_datetime datetime, OUT valid boolean)
BEGIN
  SET valid = flight_datetime > DATE_ADD(NOW(), INTERVAL -100 YEAR) AND flight_datetime < DATE_ADD(NOW(), INTERVAL 100 YEAR);
END //