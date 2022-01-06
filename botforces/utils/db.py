import aiosqlite
import datetime

"""
The DB module interacts with the database, storing, retrieving and deleting data.
"""


from botforces.utils.services import check_tags


"""
Table-creation functions.
"""


async def create_duels_table():
    """
    Creates the table to store information about ongoing duels.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute("DROP TABLE IF EXISTS duels")
    await connection.execute(
        "CREATE TABLE duels(user1_id BIGINT, user2_id BIGINT, startTime DATETIME, contestId INTEGER, contestIndex TEXT, handle1 TEXT, handle2 TEXT)"
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


async def store_duel(problem, user1, user2, handles):
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
            problem[0],
            problem[1],
            handles[1],
            handles[2],
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


async def get_problems_from_db(rating, tags):
    """
    Retrieves problems with the optional rating and tags from the database.
    """

    connection = await aiosqlite.connect("data.db")

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
            if await check_tags(problem[3], tags):
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
    cursor = await connection.execute("SELECT * FROM duels")
    duels = await cursor.fetchall()

    await cursor.close()
    await connection.close()

    return duels


async def remove_duel_from_db(duel):
    """
    Removes the duel from the database.
    """

    connection = await aiosqlite.connect("data.db")
    await connection.execute(
        "DELETE FROM duels WHERE user1_id = ? AND user2_id = ? AND startTime = ? AND contestId = ? AND contestIndex = ? AND handle1 = ? AND handle2 = ?",
        (duel[0], duel[1], duel[2], duel[3], duel[4], duel[5], duel[6]),
    )
    await connection.commit()
    await connection.close()
