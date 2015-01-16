DELIMITER //
DROP PROCEDURE IF EXISTS publications.update_num_access;
CREATE PROCEDURE publications.update_num_access(IN var_id INT)
BEGIN
	UPDATE document SET num_access=num_access+1 WHERE id=var_id;
END//