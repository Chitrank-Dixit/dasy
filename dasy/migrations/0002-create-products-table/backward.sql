BEGIN;

DELETE FROM products;
DROP TABLE IF EXISTS products;

DELETE FROM product_count;
DROP TABLE IF EXISTS product_count;

DELETE FROM migration_history WHERE name = '0002-create-products-table';

COMMIT;
