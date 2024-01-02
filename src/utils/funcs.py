"""
Contains functions used in bot.py, and which are tested in test_funcs.py
These are separated from bot.py commands in order to better faciliate unit testing
"""
def register_user(user_id):
    ...


def deregister_user(user_id):
    ...


def add_user_to_server(user_id, server_id):
    ...


def remove_user_from_server(user_id, server_id):
    ...


def remove_user_from_all_servers(user_id):
    ...


def add_sesh_for_user(user_id, day_offset=0):
    ...


def get_user_visits(user_id, last_n=None):
    ...


def graphify(data):
    ...


def get_data_for_server(server_id):
    ...


# def lastvisit(discord_ctx: DiscordCtx):
#     ...


# def table(discord_ctx: DiscordCtx):
#     ...


def get_timezone(user_id):
    ...


def set_timezone(user_id, timezone):
    ...


def update_name(user_id, new_name):
    ...


# def helpme(discord_ctx: DiscordCtx):
#     ...