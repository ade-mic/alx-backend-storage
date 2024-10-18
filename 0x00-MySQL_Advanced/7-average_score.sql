-- Assuming the table names are 'users', 'corrections', and 'average_scores'
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);

    -- Compute the average score for the user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Insert or update the average score in the average_scores table
    INSERT INTO average_scores (user_id, average_score)
    VALUES (user_id, avg_score)
    ON DUPLICATE KEY UPDATE average_score = avg_score;
END //

DELIMITER ;
