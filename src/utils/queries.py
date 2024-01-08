def user_in_db():
    ...


# selects a user by their id
SELECT_USER_IN_USERS = """\
SELECT * FROM users WHERE id = :id
"""

# register (add user into db)
INSERT_USER_INTO_USERS = """\
INSERT INTO users (id, name, added_time)
VALUES (:id, :name, :added_time)
"""

# remove user from db
REMOVE_USER_FROM_USERS = """\
DELETE FROM users
WHERE id = :id    
"""

# selects a server by its id
SELECT_SERVER_IN_SERVERS = """\
SELECT * FROM servers WHERE id = :id
"""

# add a server into servers
INSERT_SERVER_INTO_SERVERS = """\
INSERT INTO servers (id, name, added_time)
VALUES (:id, :name, :added_time)
"""

# register user with server
ADD_USER_TO_SERVER = """\
INSERT INTO user_servers (user_id, server_id)
VALUES (:user_id, :server_id)
"""

# deregister user from server
REMOVE_USER_FROM_SERVER = """\
DELETE FROM user_servers
WHERE user_id = :user_id AND server_id = :server_id
"""

# deregister user from all servers
REMOVE_USER_FROM_ALL_SERVERS = """\
DELETE FROM user_servers
WHERE user_id = :user_id    
"""

# check if a user is registered in a server
SELECT_USER_IN_SERVER = """\
SELECT * FROM user_servers WHERE user_id = :user_id AND server_id = :server_id
"""

# timezone
SELECT_USER_TIMEZONE = """\
SELECT timezone FROM users WHERE id = :id
"""

# timezone (update)
UPDATE_TIMEZONE_IN_USERS = """\
UPDATE users
SET timezone = :timezone
WHERE id = :id    
"""

# update a user's name in users
UPDATE_NAME_IN_USERS = """\
UPDATE users
SET name = :name
WHERE id = :id
"""

# show all the servers that a user is registered in
SELECT_USER_SERVERS = """\
SELECT
users.name AS name,
users.id AS discord_id,
servers.name AS server_name,
servers.id AS server_id
FROM users
INNER JOIN user_servers
ON users.id = user_servers.user_id
INNER JOIN servers
on user_servers.server_id = servers.id
WHERE users.id = :user_id
"""

# sesh
INSERT_VISIT_INTO_VISITS = """\
INSERT INTO visits (user_id, timestamp)
VALUES (:user_id, :timestamp)
"""

# get the number of visits/seshes a user has made
SELECT_COUNT_USER_VISITS = """\
SELECT
COUNT(*) AS num_visits
FROM users
INNER JOIN visits
ON users.id = visits.user_id
WHERE user_id = :user_id
"""

# retrieve a user's name
SELECT_USER_NAME_IN_USERS = """\
SELECT name FROM users
WHERE id = :id
"""

# display user data for all users in the server
# left outer join is to include users who haven't been to the gym yet.
SELECT_USER_DATA_IN_CURR_SERVER = """\
SELECT
users.name AS name,
users.id AS discord_id,
COUNT(visits.timestamp) AS timestamp
FROM users
INNER JOIN user_servers
ON users.id = user_servers.user_id
LEFT OUTER JOIN visits
ON user_servers.user_id = visits.user_id
WHERE user_servers.server_id = :server_id
GROUP BY user_servers.user_id
ORDER BY name
"""

# retrieve the date of the last visit for a given user
SELECT_LAST_N_VISITS_DATES = """\
SELECT
timestamp AS visit_date
FROM users
INNER JOIN visits
ON users.id = visits.user_id
WHERE users.id = :user_id
ORDER BY timestamp
LIMIT :n
"""