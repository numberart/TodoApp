from flask import Flask, render_template, request, session, redirect, url_for, g
import model
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'jumpingjacks'

username = ''
user = model.check_users()

# Session management

@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']

@app.route('/user')
def user():
    if "username" in session:
        user = session["username"]

@app.route('/getsession')
def getsession():
    return redirect(url_for('login'))

@app.route('/', methods= ['GET'] )
def home():
    current_user = session.get('username')
    if 'username' in session:
        g.user=session['username']
        todolists = model.unique_list(model.select_item(current_user))
        if len(todolists) == 0:
            todolists = ['-- No lists available --']
            return render_template('dashboard.html', final_list = todolists)
        else:
            return render_template('dashboard.html', final_list = todolists)
    return render_template('home.html')

# User login
@app.route('/login', methods=[ 'GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('username', None)
        are_you_user = request.form['username']
        pwd = model.check_pw(are_you_user)
        if request.form['password'] == pwd:
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        elif request.form['password'] != pwd:
            message = "Username or password incorrect."
            return render_template('login.html', message = message)
    return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('sign_up.html')
    else:
        dt = datetime.datetime.now()
        username = request.form["username"]
        password = request.form["password"]
        message = model.signup(username, password, dt)
        model.create_user_todolist(username)
        return render_template('sign_up.html', message = message)


# admin login
@app.route('/admin_login', methods = ['POST', 'GET'])
def adminlogin():
    if request.method == 'POST':
        try:
            are_you_admin = request.form["admin_username"]
            pwd = model.check_admin_pw(are_you_admin)
            if request.form['admin_password'] == pwd:
                    session['username'] = request.form['admin_username']
                    all_users = model.all_users()
                    amount_sign_ups = model.count_signups()
                    date_signups_today = model.signups_last_24()
                    user_signups_today = model.users_last_24()
                    total_amount_lists = model.total_lists(all_users)
                    return render_template('dashboardadmin.html', amount_sign_ups = amount_sign_ups, date_signups_today  = date_signups_today, users_signups_today = user_signups_today, len = len(date_signups_today), total_amount_lists = total_amount_lists)
        except:
            message = "Password or username incorrect"
            return render_template('adminpage.html', message = message)
        else:
            message = "Username or password not valid"
        return render_template('adminpage.html', message = message)
    if request.method == 'GET':
        all_users = model.all_users()
        amount_sign_ups = model.count_signups()
        date_signups_today = model.signups_last_24()
        user_signups_today = model.users_last_24()
        total_amount_lists = model.total_lists(all_users)
        return render_template('dashboardadmin.html', amount_sign_ups = amount_sign_ups, date_signups_today  = date_signups_today, users_signups_today = user_signups_today, len = len(date_signups_today), total_amount_lists = total_amount_lists)

@app.route('/adminlogout')
def adminlogout():
    session.pop('username', None)
    return redirect(url_for('admin_page'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/termsofuse')
def terms_of_use():
    return render_template('terms_of_use.html')

@app.route('/privacypage')
def privacy_page():
    return render_template('privacy_page.html')

@app.route('/adminpage', methods = ['GET', 'POST'])
def admin_page():
    return render_template('adminpage.html')

@app.route('/dashboardadmin', methods = ['GET', 'POST'])
def dashboard_admin():
    amount_sign_ups = model.count_signups()
    return render_template('dashboardadmin.html', amount_sign_ups = amount_sign_ups)

@app.route('/users_page', methods = ['GET', 'POST'])
def users_page():
    all_users = model.all_users()

    return render_template('users_page.html', all_users = all_users)

@app.route('/next_users_page<page>', methods = ['GET', 'POST'])
def next_users_page(page):
    all_users = model.all_users()
    if page == 'two':
        all_users = all_users[51:100]
    elif page == 'three':
        all_users = all_users[101:150]

    return render_template('users_page.html', all_users = all_users)

# Show users individual profile page for admin
@app.route('/userprofile/<username>', methods = ['GET', 'POST'])
def userprofile(username):
    sign_up_date = model.get_user_info(username)[0]
    all_lists = model.get_user_info(username)[1]
    return render_template('profile_page.html', username = username, sign_up_date = sign_up_date, all_lists = all_lists)

# Show users individual list items per lists for admin
@app.route('/userprofile/<username>/<name_list>', methods = ['GET', 'POST'])
def get_list_items(username, name_list):
    selected_items = model.get_all_items(username, name_list)
    return render_template('get_items_admin.html', username = username, list_name = name_list, selected_items = selected_items)

# Deletes a user from all the databases
@app.route('/delete_user/<username>', methods = ['GET', 'POST'])
def delete_user(username):
    message = model.delete_user(username)
    all_users = model.all_users()
    return render_template('users_page.html', all_users = all_users, message = message)

# todo list funcionality
@app.route('/add_list', methods = ['POST'])
def add_list():
    current_user = session.get('username')
    dt = datetime.datetime.now().date()
    list_name = request.form['add_new_list']
    model.add_list(current_user, request.form['add_new_list'], dt)
    return redirect(url_for('home'))


@app.route('/add_items', methods = ['GET', 'POST'])
def add_items():
    global name_list
    dt = datetime.datetime.now().date()
    current_user = session.get('username')
    current_item = request.form["todoitem"]
    if not current_item:
        return redirect(url_for('home'))
    model.add_item(current_user, name_list, request.form['todoitem'], dt)
    return redirect(url_for('home'))

@app.route('/complete', methods = ['POST'])
def complete():
    completed = (request.form["marked"])
    print(completed)
    current_user = session.get('username')
    conn = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM "{current_user}" WHERE item = '{completed}';""".format(completed = completed, current_user = current_user))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


@app.route('/showitems', methods = ['GET', 'POST'])
def showitems():
    global name_list
    current_user = session.get('username')
    if model.check_empty_list(current_user):
        message = "Please first create a list"
        final_list = [("No lists available")]
        return render_template('dashboard.html', current_list = final_list, message = message)
    else:
        name_list = request.form["list_items"]
    conn = sqlite3.connect('new_user_database.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute("""SELECT item FROM '{current_user}' WHERE list_name = '{name_list}';""".format(name_list = name_list, current_user = current_user))
    conn.commit()
    current_list = []
    # Remove the comma's from the string
    for i in cursor.fetchall():
        if isinstance(i[0], str):
            current_list.append(i[0])

    return render_template('show_items.html', current_list = current_list, name_list = name_list)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000,  debug = True)
