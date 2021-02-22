import sqlite3

connection = sqlite3.connect('user_database.db', check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
    """ INSERT INTO users(
    username,
    password
    )VALUES(
    'Djee',
    '123'
        );"""

)

connection.commit()
cursor.close()
connection.close()
