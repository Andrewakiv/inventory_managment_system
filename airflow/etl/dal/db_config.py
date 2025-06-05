from decouple import config

DB_CONFIG = {
    "dbname": config("PG_DB"),
    "user": config("PG_USER"),
    "password": config("PG_PASSWORD"),
    "host": config("DB_HOST"),
    "port": int(config("DB_PORT"))
}
