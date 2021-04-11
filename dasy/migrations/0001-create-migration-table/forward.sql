-- As our very first Datum migration script, this script actually creates the
-- table for recording all our migrations.

-- Note that we're using a transaction for DDL changes.  Most databases can't
-- do that.
BEGIN;
CREATE TABLE migration_history (
	name TEXT NOT NULL,
	time TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
	who TEXT DEFAULT CURRENT_USER NOT NULL,
	PRIMARY KEY (name)
);

-- All future migration scripts should have a line like this in them.  Because
-- there is a unique constraint on migration_history.name, and because this
-- insert is done in the same transaction as the DDL change, this protects you
-- from a migration accidentally being run twice.
INSERT INTO migration_history (name) VALUES ('0001-create-migrations-table');
COMMIT;
