-- script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score DECIMAL(10, 2);
    DECLARE total_weight INT;

    -- Calculate the total weighted score and total weight for the given user_id
    SELECT SUM(c.score * p.weight) INTO total_weighted_score,
           SUM(p.weight) INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Check if total_weight is not zero to avoid division by zero
    IF total_weight > 0 THEN
        -- Calculate and update the average weighted score
        UPDATE users
        SET average_score = total_weighted_score / total_weight
        WHERE id = user_id;
    ELSE
        -- If no projects are found, set average_score to 0
        UPDATE users
        SET average_score = 0
        WHERE id = user_id;
    END IF;
END //

DELIMITER ;
