--  script that creates a stored procedure
-- ComputeAverageWeightedScoreForUsers that 
-- computes and store the average weighted score for all students.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_count INT;
    DECLARE user_id INT;
    DECLARE total_weighted_score DECIMAL(10, 2);
    DECLARE total_weight INT;

    -- Declare a cursor for iterating over users
    DECLARE user_cursor CURSOR FOR 
        SELECT id FROM users;

    -- Declare a handler for when there are no more users
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET user_count = 0;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through each user
    read_loop: LOOP
        FETCH user_cursor INTO user_id;

        -- If no more users, exit the loop
        IF user_count = 0 THEN
            LEAVE read_loop;
        END IF;

        -- Calculate the total weighted score and total weight for the current user
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
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END //

DELIMITER ;
