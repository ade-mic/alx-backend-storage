-- SQL script that creates a trigger to decrease the quantity of
-- an item in the items table after a new order is added to the
-- orders table
DELIMITER //

CREATE TRIGGER after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END //

DELIMITER ;
