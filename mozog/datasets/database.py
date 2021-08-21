from playhouse.sqlite_ext import SqliteExtDatabase

from mozog.settings import DATABASE_PATH


def initialize_database(database_path: str=DATABASE_PATH) -> SqliteExtDatabase:
    database = SqliteExtDatabase(database_path, pragmas=[
        ('cache_size', -1024 * 64),
        ('journal_mode', 'wal'),
        ('foreign_keys', 1)
    ])

    return database


DATABASE = initialize_database()
