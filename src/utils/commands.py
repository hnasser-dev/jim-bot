from database import DatabaseManager, DBErrorHandler
from utils.queries import (
    SELECT_USER_IN_USERS,
    INSERT_USER_INTO_USERS,
    SELECT_SERVER_IN_SERVERS,
    INSERT_SERVER_INTO_SERVERS,
    ADD_USER_TO_SERVER,
    DEREGISTER_USER_FROM_ALL_SERVERS,
    MARK_USER_AS_INACTIVE
)
from utils.helpers import DiscordCtx, ErrorLevel
import sqlite3


class DatabaseCommandManager(DatabaseManager):
    def __init__(self, db_path):
        super().__init__(db_path)

    def register_user(self, contxt: DiscordCtx):
        user_params = {
            "id": contxt.user_id,
            "name": contxt.user_name,
            "join_time": contxt.timestamp
        }
        try:
            self.execute_query(INSERT_USER_INTO_USERS, user_params)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return DBErrorHandler(ErrorLevel.WARNING, f"User ({contxt.user_name}) already in the database.", e)
        except Exception as f:
            return DBErrorHandler(ErrorLevel.ERROR, exception=f)

    def deregister_user(self, contxt: DiscordCtx):
        users = self.execute_query(SELECT_USER_IN_USERS, {"id": contxt.user_id})
        if not users:
            return DBErrorHandler(ErrorLevel.WARNING, f"User ({contxt.user_name}) not in the database.")
        try:
            self.execute_query(DEREGISTER_USER_FROM_ALL_SERVERS, {"user_id": contxt.user_id})
            self.execute_query(MARK_USER_AS_INACTIVE, {"id": contxt.user_id})
            self.conn.commit()
        except Exception as e:
            return DBErrorHandler(ErrorLevel.ERROR, exception=e)

    def register_server(self, contxt: DiscordCtx):
        server_params = {
            "id": contxt.server_id,
            "name": contxt.server_name,
            "join_time": contxt.timestamp
        }
        try:
            self.execute_query(INSERT_SERVER_INTO_SERVERS, server_params)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return DBErrorHandler(ErrorLevel.ERROR, f"Server ({contxt.user_name}) already in the database.", e)
        except Exception as f:
            return DBErrorHandler(ErrorLevel.ERROR, exception=f)

    def add_user_to_server(self, user_id, server_id):
        ...

    def remove_user_from_server(self, user_id, server_id):
        ...

    def remove_user_from_all_servers(self, user_id):
        ...

    def add_sesh_for_user(self, user_id, day_offset=0):
        ...

    def get_user_visits(self, user_id, last_n=None):
        ...

    def graphify(self, data):
        ...

    def get_data_for_server(self, server_id):
        ...