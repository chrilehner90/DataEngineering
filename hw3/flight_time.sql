USE FlughafenDB;


DROP FUNCTION flight_time;

DELIMITER $$
CREATE FUNCTION flight_time(p_ankunft DATETIME, p_abflug DATETIME) RETURNS VARCHAR(20)
BEGIN
	DECLARE time_delta INT;
    DECLARE hours INT;
    DECLARE minutes INT;
    DECLARE hours_string VARCHAR(5);
    DECLARE minutes_string VARCHAR(7);
    DECLARE flight_time_string VARCHAR(20);
	SET time_delta = TIMESTAMPDIFF(MINUTE, p_abflug, p_ankunft);
    
    SET hours = FLOOR(time_delta / 60);
    SET minutes = time_delta % 100;
    
    IF(minutes >= 60) THEN
		SET hours = hours + 1;
        SET minutes = minutes - 60;
	END IF;
    
    # singular / plural form of hours
    IF(hours >= 2) THEN
		SET hours_string = "hours";
	ELSE
		SET hours_string = "hour";
    END IF;
    
    # singular / plural form of minutes
    IF(minutes >= 2) OR (minutes < 1) THEN
		SET minutes_string = "minutes";
	ELSE
		SET minutes_string = "minute";
    END IF;
    
    IF(hours > 0) THEN
		SET flight_time_string = CONCAT(CONVERT(hours, CHAR), " ", hours_string, ", ", CONVERT(minutes, CHAR), " ", minutes_string);
	ELSE
		SET flight_time_string = CONCAT(CONVERT(minutes, CHAR), " ", minutes_string);
	END IF;
    
    return flight_time_string;
END
$$

DELIMITER ;
SELECT f.flugnr, flight_time(f.ankunft, f.abflug) as flight_time FROM FlughafenDB.flug f;
