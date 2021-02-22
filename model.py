import sqlite3
import datetime

# verify user login
def check_pw(username):
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM users WHERE username='{username}' ORDER BY pk DESC;""".format(username=username))
    password = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()
    return password


def check_users():
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username FROM users ORDER BY pk DESC;""")
    db_users = cursor.fetchall()
    users = []

    for i in range(len(db_users)):
        person = db_users[i][0]
        users.append(person)

    connection.commit()
    cursor.close()
    connection.close()
    return users

def check_exist():
    connection = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username FROM users ORDER BY pk DESC;""")
    db_users = cursor.fetchall()
    users = []

    for i in range(len(db_users)):
        person = db_users[i][0]
        users.append(person)

    connection.commit()
    cursor.close()
    connection.close()
    return users

# verify admin login
def check_admin():
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username AND password FROM admin_data;""" )

def check_admin_pw(username):
    connection = sqlite3.connect('admin_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM admin_data WHERE username='{username}';""".format(username=username))
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return password

# Count total signups in the db
def count_signups():
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username FROM users ORDER BY pk DESC;""")
    db_users = cursor.fetchall()
    number_users = len(db_users)

    connection.commit()
    cursor.close()
    connection.close()
    return number_users

# Count signups last 24h
def signups_last_24():
    today = datetime.datetime.now()
    tdelta = datetime.timedelta(days=1)
    yesterday = today - tdelta
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT date FROM users WHERE date BETWEEN datetime('{yesterday}') AND datetime('{today}') ORDER BY pk DESC;""".format(yesterday = yesterday, today = today))
    all_dates = cursor.fetchall()
    cursor.execute(""" SELECT username FROM users WHERE date BETWEEN datetime('{yesterday}') AND datetime('{today}') ORDER BY pk DESC;""".format(yesterday = yesterday, today = today))
    all_users = cursor.fetchall()
    selected_signups = []
    for date in all_dates:
        selected_signups.append(date[0][0:19])

    connection.commit()
    cursor.close()
    connection.commit()
    return selected_signups

# Get users last 24hrs
def users_last_24():
    today = datetime.datetime.now()
    tdelta = datetime.timedelta(days=1)
    yesterday = today - tdelta
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username FROM users WHERE date BETWEEN datetime('{yesterday}') AND datetime('{today}') ORDER BY pk DESC;""".format(yesterday = yesterday, today = today))
    all_users = cursor.fetchall()
    selected_users = []
    for user in all_users:
        selected_users.append(user[0])
    connection.commit()
    cursor.close()
    connection.close()
    return selected_users

def all_users():
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username FROM users""")
    fetch_all_users = cursor.fetchall()
    all_users = []
    for user in fetch_all_users:
        all_users.append(user[0])
    connection.commit()
    cursor.close()
    connection.close()
    return all_users

# Get all personal user info
def get_user_info(username):
    # Get registration date
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT date FROM users WHERE username='{username}';""".format(username = username))
    sign_up_date = cursor.fetchone()[0][0:19]
    connection.commit()
    cursor.close()
    connection.close()

    # Get all all_lists
    connection = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT list_name FROM '{username}';""".format(username = username))
    selected_lists = cursor.fetchall()
    all_lists = []
    temp_set = set()
    for i in selected_lists:
        temp_set.add(i)
    for i in temp_set:
        all_lists.append(i[0])
        temp_set = set()
    return [sign_up_date, all_lists];

# Get all the items of a specific user for the adminpage
def get_all_items(username, list_name):
    connection = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT item FROM '{username}' WHERE list_name = '{list_name}';""".format(username = username, list_name = list_name))
    all_items = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    final_items = []
    for i in all_items:
        final_items.append(i[0])

    return final_items

# Delete user from all databases
def delete_user(username):
#    try:
    print(username)
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" DELETE FROM users WHERE username = '{username}';""".format(username = username))
    connection.commit()
    cursor.close()
    connection.close()
    connection = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" DROP TABLE '{username}';""".format(username = username))
    connection.commit()
    cursor.close()
    connection.close()
    message = "{username} was succesfully deleted from the database".format(username = username)
#    except:
        #message = "An error has occurred, please try again."

    return message



# Get total amount of list_items
def total_lists(all_users):
    connection = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    all_lists = []
    for user in all_users:
        cursor.execute(""" SELECT list_name FROM '{user}';""".format(user = user))
        selected_lists = cursor.fetchall()

        temp_set = set()
        for i in selected_lists:
            temp_set.add(i)
        for i in temp_set:
            all_lists.append(i[0])
            temp_set = set()
    connection.commit()
    cursor.close()
    connection.close()
    return len(all_lists)

# Get the lists of the individual user
def show_user_profile(username):
    connection = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT list_name FROM '{username}';""".format(username = username))
    selected_items = cursor.fetchall()
    final_lists = []
    for i in selected_lists:
        final_list.append(i[0])
    connection.commit()
    cursor.close()
    connection.close()
    return final_list

def signup(username, password, dt):
    connection = sqlite3.connect('user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM users WHERE username = '{username}';""".format(username = username))
    exist = cursor.fetchone()

    if exist is None:
        cursor.execute("""INSERT INTO users(username, password, date)VALUES('{username}', '{password}', '{dt}');""".format(username = username, password = password, dt = dt))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        return ('User already exists!')

    return 'You have succesfully signed up!'


def run_query(query, parameters = ()):
    with sqlite3.connect('user_database.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
        cursor.close()
        return result

# create the table when the user creates it's first todo list
### Create a table that incorporates the username, date, name of the todo list
def create_user_todolist(current_user):
    connection = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE '{current_user}'(
           list_name VARCHAR(32),
           date INTEGER,
           item VARCHAR(32)
           );""".format(current_user = current_user)
           )
    connection.commit()
    cursor.close()
    connection.close()

def add_list(username, list_name, dt):
    conn = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO '{username}'(list_name, date)VALUES('{list_name}', '{dt}');""".format(username = username, list_name = list_name, dt = dt))
    conn.commit()
    cursor.close()
    conn.close()


def add_item(current_user, list_name, item, dt):
    conn = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO '{current_user}'(list_name, date, item)VALUES('{list_name}','{dt}', '{item}');""".format(current_user = current_user, list_name = list_name, item = item, dt = dt))
    conn.commit()
    cursor.close()
    conn.close()



def select_item(username):
    conn = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = conn.cursor()
    all_items = cursor.execute("""SELECT list_name FROM '{username}';""".format(username = username))
    todolist = []
    for list in all_items:
        todolist.append(list[0])
    final_list = unique_list(todolist)
    conn.commit()
    cursor.close()
    conn.close()

    return todolist


def unique_list(list):
    unique_list = []
    for i in list:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list

def check_empty_list(username):
    conn = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute("""SELECT list_name FROM '{username}'""".format(username = username))
    all_lists = cursor.fetchall()
    if len(all_lists) == 0:
        return True
    else:
        return False
