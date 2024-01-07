from src.database import DatabaseManager
from src.utils.error_handling import DatabaseError, OtherError
from src.utils.helpers import DiscordCtx, ExecutionOutcome, DayOffset
from src.utils.globals import BOT_PREFIX
import sqlite3
from src.utils.queries import (
    SELECT_USER_IN_USERS,
    INSERT_USER_INTO_USERS,
    REMOVE_USER_FROM_USERS,
    SELECT_SERVER_IN_SERVERS,
    INSERT_SERVER_INTO_SERVERS,
    ADD_USER_TO_SERVER,
    ADD_USER_TO_SERVER,
    REMOVE_USER_FROM_SERVER,
    REMOVE_USER_FROM_ALL_SERVERS,
    SELECT_USER_IN_SERVER,
    SELECT_USER_SERVERS,
    SELECT_USER_TIMEZONE,
    UPDATE_TIMEZONE_IN_USERS,
    UPDATE_NAME_IN_USERS,
    SELECT_USER_NAME_IN_USERS,
    INSERT_VISIT_INTO_VISITS,
    SELECT_COUNT_USER_VISITS,
    SELECT_USER_DATA_IN_CURR_SERVER,
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

    def add_user_to_users(self, contxt: DiscordCtx):
        user_params = {
            "id": contxt.user_id,
            "name": contxt.user_name,
            "added_time": contxt.timestamp
        }
        try:
            self.execute_query(INSERT_USER_INTO_USERS, user_params)
        except sqlite3.IntegrityError as e:
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) already in the database.", e)
        except sqlite3.Error as f:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=f)

    def remove_user_from_users(self, contxt: DiscordCtx):
        if not self.user_in_db(contxt.user_id):
            print("User not in db")
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) not in the database.")
        try:
            self.execute_query(REMOVE_USER_FROM_USERS, {"id": contxt.user_id})
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)
        print("User removed")

    def register_server(self, contxt: DiscordCtx):
        server_params = {
            "id": contxt.server_id,
            "name": contxt.server_name,
            "added_time": contxt.timestamp
        }
        try:
            self.execute_query(INSERT_SERVER_INTO_SERVERS, server_params)
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
        except sqlite3.IntegrityError as e:
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) already registered in this server.", e)
        except sqlite3.Error as f:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=f)

    def remove_user_from_server(self, contxt: DiscordCtx):
        params = {
            "user_id": contxt.user_id,
            "server_id": contxt.server_id,
        }     
        if not self.server_in_db(contxt.server_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING,
                f"This is not a registered server. Use `{BOT_PREFIX}registerserver` to register this server first."
        )       
        try:
            user_results = self.execute_query(SELECT_USER_IN_SERVER, params)
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)
        else:
            if len(user_results) < 1:
                return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) is not registered in this server.")
        try:
            self.execute_query(REMOVE_USER_FROM_SERVER, params)
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
        except sqlite3.Error as f:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=f)

    def get_timezone(self, contxt: DiscordCtx):
        if not self.user_in_db(contxt.user_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) not in the database.")
        timezone = self.execute_query(SELECT_USER_TIMEZONE, {"id": contxt.user_id})
        return timezone

    def set_timezone(self, contxt: DiscordCtx, timezone_id: str):
        if not self.user_in_db(contxt.user_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) not in the database.")
        try:
            self.execute_query(UPDATE_TIMEZONE_IN_USERS, {"id": contxt.user_id, "timezone": timezone_id})
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)
        return timezone_id

    def update_name(self, contxt: DiscordCtx):
        try:
            user_results = self.execute_query(SELECT_USER_NAME_IN_USERS, {"id": contxt.user_id})
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)
        else:
            if len(user_results) < 1:
                return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) is not registered in this server.")
        old_username = user_results[0]
        if old_username == contxt.user_name:
            return OtherError(contxt, ExecutionOutcome.ERROR, f"Your current username ({contxt.user_name}) is the same as your currently-registered username ({old_username}).")
        try:
            new_name = self.execute_query(UPDATE_NAME_IN_USERS, {"id": contxt.user_id})[0]
        except sqlite3.Error as e:
            return DatabaseError(contxt, ExecutionOutcome.ERROR, exception=e)
        return new_name

    def add_sesh_for_user(self, contxt: DiscordCtx, offset=0):
        try:
            day_offset = DayOffset(offset)
        except ValueError as e: # if not a valid value
            return OtherError(contxt, ExecutionOutcome.WARNING, f"Must supply a valid date offset (between -7 and 0 inclusive).")
        timestamp = contxt.get_timestamp_str(day_offset=day_offset.value)
        user_params = {
            "user_id": contxt.user_id,
            "timestamp": timestamp
        }
        if not self.user_in_db(contxt.user_id):
            return DatabaseError(contxt, ExecutionOutcome.WARNING, f"User ({contxt.user_name}) not in the database.")
        try:
            self.execute_query(INSERT_VISIT_INTO_VISITS, user_params)
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
        params = {
            "server_id": contxt.server_id
        }
        data = self.execute_query(SELECT_USER_DATA_IN_CURR_SERVER, params)
        print(data)