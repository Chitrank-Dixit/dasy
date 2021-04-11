BEGIN;

CREATE TABLE products (
    sku TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE product_count (
    name TEXT PRIMARY KEY NOT NULL,
    no_of_products INTEGER DEFAULT 0
);

-- CREATE OR REPLACE FUNCTION product_entry_trigger() RETURNS TRIGGER AS $$
-- DECLARE
--     i_no_of_products INTEGER;
--     r_no_of_products INTEGER;
-- BEGIN
--     SELECT COUNT(*) INTO i_no_of_products FROM products WHERE "name" = NEW.name GROUP BY "name";
--     IF (TG_OP = 'INSERT') THEN
--       IF EXISTS (SELECT no_of_products FROM product_count WHERE "name" = NEW.name) THEN
--         SELECT no_of_products INTO r_no_of_products FROM product_count WHERE "name" = NEW.name;
--         UPDATE product_count set no_of_products = r_no_of_products + 1 WHERE "name" = NEW.name;
--       ELSE
--         INSERT INTO product_count (name, no_of_products) values (NEW.name, i_no_of_products);
--       END IF;
--     ELSEIF (TG_OP = 'UPDATE') THEN
--       UPDATE product_count set no_of_products = i_no_of_products WHERE "name" = NEW.name;
--     END IF;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;
--
-- CREATE TRIGGER product_entry_trigger
-- AFTER UPDATE OR INSERT
-- ON products
-- FOR EACH ROW EXECUTE PROCEDURE product_entry_trigger();

INSERT INTO migration_history VALUES ('0002-create-products-table');

COMMIT;
