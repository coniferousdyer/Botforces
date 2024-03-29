"""
The DB module interacts with the database, storing, retrieving and deleting data.
"""


import aiosqlite
import datetime

from botforces.utils.services import check_tags


"""
Table-creation functions.
"""


async def create_users_table():
    """
    Creates the table to store mappings of Discord usernames and Codeforces handles.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute(
        "CREATE TABLE IF NOT EXISTS users(discord_id BIGINT, handle TEXT)"
    )
    await connection.commit()
    await connection.close()


async def create_duels_table():
    """
    Creates the table to store information about ongoing duels.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute("DROP TABLE IF EXISTS duels")
    await connection.execute(
        "CREATE TABLE duels(user1_id BIGINT, user2_id BIGINT, startTime DATETIME, contestId INTEGER, contestIndex TEXT, handle_1 TEXT, handle_2 TEXT)"
    )
    await connection.commit()
    await connection.close()


async def create_contests_table():
    """
    Creates the table to store information about upcoming contests.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute("DROP TABLE IF EXISTS contests")
    await connection.execute(
        "CREATE TABLE contests(id INTEGER, name TEXT, durationSeconds BIGINT, startTimeSeconds BIGINT)"
    )
    await connection.commit()
    await connection.close()


async def create_problems_table():
    """
    Creates the table to store information about problems.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute("DROP TABLE IF EXISTS problems")
    await connection.execute(
        "CREATE TABLE problems(contestId INTEGER, contestIndex TEXT, name TEXT, tags TEXT, rating INTEGER)"
    )
    await connection.commit()
    await connection.close()


"""
Database insertion functions.
"""


async def store_user(discord_id, handle):
    """
    Stores the Discord ID-Codeforces handle mapping in the database.
    """

    connection = await aiosqlite.connect("data.db")

    # Checking if the user already exists in the database
    cursor = await connection.execute(
        "SELECT * FROM users WHERE discord_id = ?", (discord_id,)
    )
    user = await cursor.fetchone()
    await cursor.close()

    # If the user exists, update the handle
    if user:
        await connection.execute(
            "UPDATE users SET handle = ? WHERE discord_id = ?",
            (handle, discord_id),
        )
        await connection.commit()
        await connection.close()
        return

    await connection.execute("INSERT INTO users VALUES(?, ?)", (discord_id, handle))
    await connection.commit()
    await connection.close()


async def store_duel(problem, user1, user2, handle_1, handle_2):
    """
    Stores the duel in the database.
    """

    # Storing the start time of the duel
    startTime = datetime.datetime.now()

    connection = await aiosqlite.connect("data.db")
    await connection.execute(
        "INSERT INTO duels VALUES(?, ?, ?, ?, ?, ?, ?)",
        (
            user1.id,
            user2.id,
            startTime,
            problem["contestId"],
            problem["contestIndex"],
            handle_1,
            handle_2,
        ),
    )
    await connection.commit()
    await connection.close()


async def store_contest(contest):
    """
    Stores the upcoming contest in the database.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute(
        "INSERT INTO contests VALUES(?, ?, ?, ?)",
        (
            contest["id"],
            contest["name"],
            contest["durationSeconds"],
            contest["startTimeSeconds"],
        ),
    )
    await connection.commit()
    await connection.close()


async def store_problem(problem):
    """
    Stores the problem in the database.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute(
        "INSERT INTO problems VALUES(?, ?, ?, ?, ?)",
        (
            problem["contestId"],
            problem["index"],
            problem["name"],
            repr(problem["tags"]),
            problem["rating"],
        ),
    )
    await connection.commit()
    await connection.close()


"""
Database retrieval functions.
"""


async def get_handle_from_db(discord_id):
    """
    Retrieves the handle of the user from the database.
    """

    connection = await aiosqlite.connect("data.db")
    connection.row_factory = aiosqlite.Row
    cursor = await connection.execute(
        "SELECT * FROM users WHERE discord_id = ?", (discord_id,)
    )
    user = await cursor.fetchone()
    await cursor.close()
    await connection.close()

    return user["handle"] if user else None


async def get_problems_from_db(rating, tags):
    """
    Retrieves problems with the optional rating and tags from the database.
    """

    connection = await aiosqlite.connect("data.db")
    connection.row_factory = aiosqlite.Row

    # Reading the problems of rating (if mentioned) into a list
    if rating != 0:
        cursor = await connection.execute(
            "SELECT * FROM problems WHERE rating = ?", (rating,)
        )
        problemList = await cursor.fetchall()
    else:
        cursor = await connection.execute("SELECT * FROM problems")
        problemList = await cursor.fetchall()

    # If tags were given, i.e. tags is not empty, check tags and add it to the final list
    finalList = []
    if tags != []:
        for problem in problemList:
            if await check_tags(problem["tags"], tags):
                finalList.append(problem)

        problemList = finalList

    await cursor.close()
    await connection.close()

    return problemList


async def get_contests_from_db():
    """
    Retrieves the upcoming contests from the database.
    """

    connection = await aiosqlite.connect("data.db")
    connection.row_factory = aiosqlite.Row
    cursor = await connection.execute("SELECT * from contests")
    contestList = await cursor.fetchall()
    await cursor.close()
    await connection.close()

    return contestList


async def get_duel_from_db(user_requesting):
    """
    Retrieves the duel from the database.
    """

    connection = await aiosqlite.connect("data.db")
    connection.row_factory = aiosqlite.Row
    cursor = await connection.execute(
        "SELECT * FROM duels WHERE user1_id = ? OR user2_id = ?",
        (user_requesting.id, user_requesting.id),
    )
    duel = await cursor.fetchone()

    await cursor.close()
    await connection.close()

    return duel


async def get_duels_from_db():
    """
    Retrieves all duels from the database.
    """

    connection = await aiosqlite.connect("data.db")
    connection.row_factory = aiosqlite.Row
    cursor = await connection.execute("SELECT * FROM duels")
    duels = await cursor.fetchall()

    await cursor.close()
    await connection.close()

    return duels


"""
Database deletion functions.
"""


async def remove_user_from_db(discord_id):
    """
    Removes the Discord ID-Codeforces handle mapping from the database.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute("DELETE FROM users WHERE discord_id = ?", (discord_id,))
    await connection.commit()
    await connection.close()


async def remove_duel_from_db(duel):
    """
    Removes the duel from the database.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute(
        "DELETE FROM duels WHERE user1_id = ? AND user2_id = ?",
        (duel["user1_id"], duel["user2_id"]),
    )
    await connection.commit()
    await connection.close()
