def user_in_db():
    ...


# selects a user by their id
SELECT_USER_IN_USERS = """\
SELECT * FROM users WHERE id = :id
"""