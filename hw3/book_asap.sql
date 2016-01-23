use flughafen;

DROP PROCEDURE IF EXISTS book_asap;

DELIMITER $$
CREATE PROCEDURE book_asap(IN v_von VARCHAR(3), IN v_nach VARCHAR(3), IN v_abflug DATETIME, IN v_passnummer VARCHAR(20))
BEGIN
	DECLARE v_flug_id INT(11);
    DECLARE v_flugnr VARCHAR(10);
    DECLARE v_passagier_id INT(11);
    DECLARE v_flughafen_id_von INT(11);
    DECLARE v_flughafen_id_nach INT(11);
    
    declare v_test int(11);
    
    SELECT flughafen_id INTO v_flughafen_id_von FROM flughafen WHERE iata = v_von;
    SELECT flughafen_id INTO v_flughafen_id_nach FROM flughafen WHERE iata = v_nach;
    
	SELECT 
		f.flug_id, f.flugnr, fz.kapazitaet INTO v_flug_id, v_flugnr, v_test
	FROM
		flug AS f
			INNER JOIN
		buchung AS b ON (f.flug_id = b.flug_id)
			INNER JOIN
		flugzeug AS fz ON (f.flugzeug_id = fz.flugzeug_id)
	WHERE
		f.von = v_flughafen_id_von 
        AND f.nach = v_flughafen_id_nach
		AND f.abflug >= v_abflug
	GROUP BY f.flug_id
	HAVING COUNT(b.buchung_id) < fz.kapazitaet
	ORDER BY f.ankunft ASC
    LIMIT 1;
    
    IF v_flug_id THEN
		SELECT passagier_id INTO v_passagier_id FROM passagier WHERE passnummer = v_passnummer;
        IF v_passagier_id THEN
			INSERT INTO buchung(flug_id, passagier_id, preis) VALUES(v_flug_id, v_passagier_id, 100.00);
			SELECT CONCAT('A seat from ', v_von, ' to ', v_nach,' was booked on flight ', v_flugnr) AS booked;
		ELSE
			SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Sorry, wrong passenger ID';
        END IF;
	ELSE		
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Sorry, no flight available';
	END IF;
END $$
DELIMITER ;

# Success Call
CALL book_asap('LDN', 'PRP', '2000-1-1 00:00:01', 'P103022');

# Error Call
CALL book_asap('SBG', 'VIE', '2000-1-1 00:00:01', 'P103022');




