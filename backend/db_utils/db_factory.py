from enum import Enum
from db_utils.connections import SQLiteConnection


class DBType(Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRES = "postgres"

db_configs = {
    DBType.SQLITE: {
        "NAME": "db.sqlite3",
    },
    DBType.POSTGRES: {
        "NAME": "my_postgres_db",
        "USER": "postgres_user",
        "PASSWORD": "postgres_pass",
        "HOST": "hostname",
        "PORT": "portnum",
    },
}


class DBFactory:
    @staticmethod
    def get_db_connection(db_type):
        if db_type == DBType.SQLITE:
            return SQLiteConnection(db_configs[DBType.SQLITE])
        elif db_type == DBType.POSTGRES:
            return SQLiteConnection(db_configs[DBType.POSTGRES])
        else:
            raise ValueError("Unsupported database type")