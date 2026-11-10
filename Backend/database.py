import sqlite3
import sys
from pathlib import Path


project_folder = Path(__file__).resolve().parent.parent
database_folder = Path(sys.executable).parent if getattr(sys, 'frozen', False) else project_folder
database_file = database_folder / "Database SQLite" / "canteen.db"


def connect_database():
    # Open an existing database. Create tables manually in DB Browser.
    database_url = database_file.resolve().as_uri() + "?mode=rw"
    connection = sqlite3.connect(database_url, uri=True)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def upgrade_database():
    """Add missing columns without deleting existing records."""
    connection = connect_database()
    additions = {
        'users': {'is_approved': 'INTEGER NOT NULL DEFAULT 0', 'is_suspended': 'INTEGER NOT NULL DEFAULT 0'},
        'shops': {'opening_time': "TEXT NOT NULL DEFAULT '06:45'", 'closing_time': "TEXT NOT NULL DEFAULT '16:00'", 'slot_capacity': 'INTEGER NOT NULL DEFAULT 10'},
        'orders': {'request_id': 'TEXT', 'request_payload': 'TEXT', 'is_overdue': 'INTEGER NOT NULL DEFAULT 0'},
        'menu_items': {'image_path': "TEXT NOT NULL DEFAULT ''"},
    }
    try:
        missing = any(name not in {row[1] for row in connection.execute(f'PRAGMA table_info({table})')} for table, columns in additions.items() for name in columns)
        actual_file = connection.execute('PRAGMA database_list').fetchone()[2]
        if missing and actual_file:
            from datetime import datetime
            folder = Path(actual_file).parent / 'backups'
            folder.mkdir(exist_ok=True)
            backup_file = folder / (datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.db')
            backup = sqlite3.connect(backup_file)
            try:
                connection.backup(backup)
            finally:
                backup.close()
        with connection:
            connection.execute('BEGIN IMMEDIATE')
            for table, columns in additions.items():
                existing = {row[1] for row in connection.execute(f'PRAGMA table_info({table})')}
                for name, definition in columns.items():
                    if name not in existing:
                        connection.execute(f'ALTER TABLE {table} ADD COLUMN {name} {definition}')
            connection.execute('CREATE UNIQUE INDEX IF NOT EXISTS order_request_unique ON orders(user_id, request_id)')
            connection.execute('CREATE TABLE IF NOT EXISTS login_attempts (username TEXT PRIMARY KEY, failures INTEGER NOT NULL, locked_until REAL NOT NULL)')
    finally:
        connection.close()
