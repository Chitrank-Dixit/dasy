-- This script allows undoing the changes done in the corresponding
-- 'forwards.sql' script.  Hopefully it won't be needed.
BEGIN;

-- Technically we could skip the deletion of this row, since we're actually
-- going to be dropping the migration_history table.  But this is here to
-- demonstrate that backwards.sql migrations are responsible for deleting their
-- corresponding rows in the migration_history table.
DELETE from migration_history where name='0001-create-migrations-table';

-- The actual DDL change we're making.
DROP TABLE migration_history;

COMMIT;
