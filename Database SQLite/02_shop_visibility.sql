-- Existing databases only. Run once; new schema.sql already includes this column.
PRAGMA foreign_keys = ON;
SAVEPOINT shop_visibility;
ALTER TABLE shops ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1
    CHECK(is_active IN (0, 1));
RELEASE SAVEPOINT shop_visibility;
