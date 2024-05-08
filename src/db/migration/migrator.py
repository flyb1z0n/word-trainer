migrator_create = """
    CREATE TABLE IF NOT EXISTS schema_history (
    version INTEGER NOT NULL
    );
"""

class Migrator:

        