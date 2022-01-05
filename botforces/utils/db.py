import sqlite3

from botforces.utils.services import check_tags


"""
Table-creation functions.
"""


def create_duels_table():
    """
    Creates the table to store information about ongoing duels.
    """

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS duels")
    cursor.execute(
        "CREATE TABLE duels(user1_id BIGINT, user2_id BIGINT, startTime DATETIME, contestId INTEGER, contestIndex TEXT, handle1 TEXT, handle2 TEXT)"
    )
    connection.commit()
    connection.close()


def create_contests_table():
    """
    Creates the table to store information about upcoming contests.
    """

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS contests")
    cursor.execute(
        "CREATE TABLE contests(id INTEGER, name TEXT, durationSeconds BIGINT, startTimeSeconds BIGINT)"
    )
    connection.commit()
    connection.close()


def create_problems_table():
    """
    Creates the table to store information about problems.
    """

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS problems")
    cursor.execute(
        "CREATE TABLE problems(contestId INTEGER, contestIndex TEXT, name TEXT, tags TEXT, rating INTEGER)"
    )
    connection.commit()
    connection.close()


"""
Database insertion functions.
"""


def store_contest(contest):
    """
    Stores the upcoming contest in the database.
    """

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO contests VALUES(?, ?, ?, ?)",
        (
            contest["id"],
            contest["name"],
            contest["durationSeconds"],
            contest["startTimeSeconds"],
        ),
    )
    connection.commit()
    connection.close()


def store_problem(problem):
    """
    Stores the problem in the database.
    """

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO problems VALUES(?, ?, ?, ?, ?)",
        (
            problem["contestId"],
            problem["index"],
            problem["name"],
            repr(problem["tags"]),
            problem["rating"],
        ),
    )
    connection.commit()
    connection.close()


"""
Database retrieval functions.
"""


def get_problems_from_db(rating, tags):
    """
    Retrieves problems with the optional rating and tags from the database.
    """

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    # Reading the problems of rating (if mentioned) into a list
    if rating != 0:
        problemList = cursor.execute(
            "SELECT * FROM problems WHERE rating = ?", (rating,)
        ).fetchall()
    else:
        problemList = cursor.execute("SELECT * FROM problems").fetchall()

    # If tags were given, i.e. tags is not empty, check tags and add it to the final list
    finalList = []
    if tags != []:
        for problem in problemList:
            if check_tags(problem[3], tags):
                finalList.append(problem)

        problemList = finalList

    connection.close()
    return problemList


def get_contests_from_db():
    """
    Retrieves the upcoming contests from the database.
    """

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    contestList = cursor.execute("SELECT * from contests").fetchall()
    connection.close()
    
    return contestList