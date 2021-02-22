import sqlite3

connection = sqlite3.connect('user_database.db', check_same_thread = False)
cursor = connection.cursor()


cursor.execute(
    """CREATE TABLE todolist(
       id INTEGER PRIMARY KEY,
       username VARCHAR(32),
       item VARCHAR(32),
       completed INTEGER NOT NULL,
       FOREIGN KEY(username) REFERENCES users(username) ON DELETE SET NULL
       );"""
)


def run_query(query, parameters = ()):
    with sqlite3.connect('user_database.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
        return result



connection.commit()
cursor.close()
connection.close()
