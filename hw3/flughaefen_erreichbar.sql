use FlughafenDB;

SET max_sp_recursion_depth = 20;

DROP PROCEDURE IF EXISTS erreichbare_flughaefen;

DELIMITER $$
CREATE PROCEDURE erreichbare_flughaefen(IN p_flughafen_id INT, IN p_max_hops INT, IN p_num_hops INT)
BEGIN
	DECLARE v_ziel INT;
	DECLARE v_i INT DEFAULT 0;
	DECLARE v_n INT DEFAULT 0;
	DECLARE v_num_hops INT DEFAULT 0;

	IF(p_num_hops = 0)  THEN
		DROP TABLE IF EXISTS flughafen_erreichbar;
		CREATE TABLE flughafen_erreichbar (
			flughafen_id INTEGER PRIMARY KEY,
			hops INTEGER
		);
	END IF;

	IF(p_num_hops > p_max_hops) then
		SELECT 'FINISHED';
	ELSE
		INSERT INTO flughafen_erreichbar SELECT nach, p_num_hops FROM flug WHERE von = p_flughafen_id GROUP BY nach;
		SELECT COUNT(DISTINCT nach) FROM flug WHERE von = p_flughafen_id INTO v_n;
		WHILE v_i < v_n DO
			SELECT nach FROM flug WHERE von = p_flughafen_id GROUP BY nach LIMIT v_i, 1 INTO v_ziel;

			SET v_num_hops = p_num_hops + 1;

			CALL erreichbare_flughaefen(v_ziel, p_max_hops, v_num_hops);

			SET v_i = v_i + 1;
		END WHILE;
	END IF;
END
$$
DELIMITER ;

CALL erreichbare_flughaefen(4018, 2, 0);
select * from flughafen_erreichbar ORDER BY hops;