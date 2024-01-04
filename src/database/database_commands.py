from src.database import DatabaseManager
from src.utils.error_handling import DatabaseError, ParseError
from src.utils.helpers import DiscordCtx, ExecutionOutcome, DayOffset
from src.utils.globals import BOT_PREFIX
import sqlite3
from src.utils.queries import (
    SELECT_USER_IN_USERS,
    INSERT_USER_INTO_USERS,
    SELECT_SERVER_IN_SERVERS,
    INSERT_SERVER_INTO_SERVERS,
    ADD_USER_TO_SERVER,
    MARK_USER_AS_INACTIVE,
    ADD_USER_TO_SERVER,
    REMOVE_USER_FROM_SERVER,
    REMOVE_USER_FROM_ALL_SERVERS,
    SELECT_USER_IN_SERVER,
    SELECT_USER_SERVERS,
    INSERT_VISIT_INTO_VISITS,
    SELECT_COUNT_USER_VISITS,
    SELECT_USER_TIMEZONE,
    UPDATE_TIMEZONE_IN_USERS
)


class DatabaseCommands(DatabaseManager):
    def __init__(self, db_path):
        super().__init__(db_path)

    def user_in_db(self, user_id) -> bool:
        users = self.execute_query(SELECT_USER_IN_USERS, {"id": user_id})
        return bool(users)
    
    def server_in_db(self, server_id) -> bool:
        servers = self.execute_query(SELECT_SERVER_IN_SERVERS, {"id": server_id})
        return bool(servers)

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
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) already in the database.", e)
        except sqlite3.Error as f:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=f)

    def mark_user_as_inactive(self, contxt: DiscordCtx):
        if not self.user_in_db(contxt.user_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) not in the database.")
        try:
            self.execute_query(MARK_USER_AS_INACTIVE, {"id": contxt.user_id})
            self.conn.commit()
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)

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
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"This server is already registered.", e)
        except sqlite3.Error as f:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=f)

    def add_user_to_server(self, contxt: DiscordCtx):
        params = {
            "user_id": contxt.user_id,
            "server_id": contxt.server_id,
        }
        if not self.server_in_db(contxt.server_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING,
                f"This is not a registered server. Use `{BOT_PREFIX}registerserver` to register this server first."
            )
        try:
            self.execute_query(ADD_USER_TO_SERVER, params)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) already registered in this server.", e)
        except sqlite3.Error as f:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=f)

    def remove_user_from_server(self, contxt: DiscordCtx):
        params = {
            "user_id": contxt.user_id,
            "server_id": contxt.server_id,
        }
        try:
            user_results = self.execute_query(SELECT_USER_IN_SERVER, params)
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)
        else:
            if len(user_results) < 1:
                return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) is not registered in this server.")
        try:
            self.execute_query(REMOVE_USER_FROM_SERVER, params)
            self.conn.commit()
        except sqlite3.Error as f:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=f)

    def remove_user_from_all_servers(self, contxt: DiscordCtx):
        params = {
            "user_id": contxt.user_id,
        }
        try:
            user_results = self.execute_query(SELECT_USER_SERVERS, params)
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)
        else:
            if len(user_results) < 1:
                return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) is not registered in any servers.")
        try:
            self.execute_query(REMOVE_USER_FROM_ALL_SERVERS, params)
            self.conn.commit()
        except sqlite3.Error as f:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=f)

    def get_timezone(self, contxt: DiscordCtx):
        if not self.user_in_db(contxt.user_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) not in the database.")
        timezone = self.execute_query(SELECT_USER_TIMEZONE, {"id": contxt.user_id})
        return timezone

    def set_timezone(self, contxt: DiscordCtx, timezone):
        if not self.user_in_db(contxt.user_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) not in the database.")
        # TODO - parse the timezone the user provided
        try:
            self.execute_query(UPDATE_TIMEZONE_IN_USERS, {"id": contxt.user_id})
            self.conn.commit()
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)
        return timezone

    def add_sesh_for_user(self, contxt: DiscordCtx, offset=0):
        try:
            day_offset = DayOffset(offset)
        except ValueError as e: # if not a valid value
            return ParseError(contxt, ExecutionOutcome.WARNING, f"Must supply a valid date offset (between -7 and 0 inclusive).")
        timestamp = contxt.get_timestamp_str(day_offset=day_offset.value)
        user_params = {
            "user_id": contxt.user_id,
            "timestamp": timestamp
        }
        if not self.user_in_db(contxt.user_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) not in the database.")
        try:
            self.execute_query(INSERT_VISIT_INTO_VISITS, user_params)
            self.conn.commit()
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)
        return self.get_user_visits(contxt=contxt) # return the updated number of visits

    def get_user_visits(self, contxt: DiscordCtx) -> int|DatabaseError:
        user_params = {
            "user_id": contxt.user_id
        }
        if not self.user_in_db(contxt.user_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) not in the database.")
        num_visits = self.execute_query(SELECT_COUNT_USER_VISITS, user_params)[0]
        return num_visits

    def graphify(self, contxt: DiscordCtx):
        ...

    def get_data_for_server(self, contxt: DiscordCtx):
        ...