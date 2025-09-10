# config/database_config.py
DATABASE_CONFIG = {
    "user": "team5hack",
    "password": "IneedApa$$word",
    "host": "team5-postgres-db.postgres.database.azure.com",
    "port": 5432,
    "database": "postgres",
    "sslmode": "require"
}

SCHEMA_SUFFIX = "_dummydata"  # or "" for production
