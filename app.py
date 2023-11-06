from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta, time

app = Flask(__name__)

app.secret_key = 'd9e523fba0ebfeebaafc1a46b2702472a160ebb03c47f4b938b5554272dd536d'

if __name__ == '__main__':
    app.run(debug=True)

# Da die Zugangsdaten für die phpMyAdmin-Seite nicht öffentlich zugänglich sein sollen,
# sind die nötigen Information zur Verbindung mit der Datenbank in den Strings nicht enthalten.
# Dafür ist ein create_db.sql Datei enthalten, mit der man die Datenbank nachkreieren kann.
# Die benötigten Verbindungsdaten müssen dann hier eingetragen werden.

app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''


mysql = MySQL(app)
bcrypt = Bcrypt(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    daily_total = '-'
    weekly_total = '-'
    general_total = '-'
    daily_rate = '-'
    if 'username' in session:
        username = session['username']
        today = datetime.combine(datetime.now(), time.min)
        last_week = datetime.now() - timedelta(weeks=1)
        cur = mysql.connection.cursor()
        cur.execute("SELECT username, answers_total, answers_right FROM tbl_progress WHERE username=%s AND solved_at>=%s", (username, today,))
        daily_stats = cur.fetchall()
        cur.execute("SELECT username, answers_total, answers_right FROM tbl_progress WHERE username=%s AND solved_at>=%s", (username, last_week,))
        weekly_stats = cur.fetchall()
        cur.execute("SELECT username, answers_total, answers_right FROM tbl_progress WHERE username=%s", (username,))
        general_stats = cur.fetchall()
        cur.close()
        daily_total = len(daily_stats)
        weekly_total = len(weekly_stats)
        general_total = len(general_stats)
        daily_answers_total = 0
        daily_answers_right = 0
        if daily_stats:
            for i in daily_stats:
                daily_answers_total = daily_answers_total + i[1]
                daily_answers_right = daily_answers_right + i[2]
            daily_rate = str(round(daily_answers_right / daily_answers_total * 100, 1))+'%'
    return render_template('home.html', daily_total=daily_total, weekly_total=weekly_total, general_total=general_total,
                           daily_rate=daily_rate)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            error = 'Du hast nicht alles ausgefüllt'
        else:
            cur = mysql.connection.cursor()
            # angreifbare Datenbankabfragen:
            # 1.    cur.execute("SELECT username, password FROM sql_injection_test WHERE username="+username)
            # 2.    cur.execute("SELECT username, password FROM sql_injection_test WHERE username='%s' % username")
            cur.execute("SELECT username, password_hash FROM tbl_users WHERE username=%s", (username,))
            user = cur.fetchone()
            cur.close()
            password_is_valid = bcrypt.check_password_hash(user[1], password)
            if user and password_is_valid:
                session['username'] = user[0]
                return redirect(url_for('home'))
            else:
                error = 'Benutzername oder Kennwort ungültig'
        flash(error)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        email = request.form['email']
        error = None
        cur = mysql.connection.cursor()
        # angreifbar -> cur.execute("SELECT username FROM sql_injection_test WHERE username="+username)
        cur.execute("SELECT username FROM tbl_users WHERE username= %s",(username,))
        user_exists = cur.fetchone()
        cur.close()
        if not username or not password or not email:
            error = 'Du hast nicht alles ausgefüllt.'
        elif len(username) > 20:
            error = 'Der Benutzername darf nicht mehr als 20 Zeichen enthalten.'
        elif len(password) > 50:
            error = 'Das Passwort darf nicht mehr als 50 Zeichen enthalten.'
        elif len(email) > 254:
            error = 'Die Email-Adresse ist zu lang'
        elif not password_repeat:
            error = 'Du hast das Passwort nicht bestätigt'
        elif user_exists:
            error = 'Der Benutzername ist leider bereits vergeben'
        elif password_repeat != password:
            error = '"Passwort" und "Passwort Bestätigung" stimmen nicht überein'
        if error is None:
            cur = mysql.connection.cursor()
            # angreifbar -> cur.execute("INSERT INTO sql_injection_test(username, password) VALUES ("+username+", "+password+")")
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cur.execute("INSERT INTO tbl_users(username, password_hash, email) VALUES (%s, %s, %s)",
                (username, hashed_password, email,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('home'))
        flash(error)
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/uebungen', methods=['GET'])
def uebungen():
        return render_template('/uebungen.html')


@app.route('/uebungen/<aufgabe>', methods=['GET', 'POST'])
def aufgaben(aufgabe):
    if request.method == 'POST':
        if 'username' in session:
            result = request.get_json()
            username = session.get('username')
            answers_right = result.get('answers_right')
            answers_total = result.get('answers_total')
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tbl_progress(username, answers_total, answers_right) VALUES (%s, %s, %s)", (username, answers_total, answers_right,))
            mysql.connection.commit()
            cur.close()
        return jsonify()
    js_file = "../static/%s.js" % aufgabe
    return render_template('/aufgabe.html', js_file=js_file)


@app.route('/theorie', methods=['GET'])
def theorie():
    return render_template('/theorie.html')


@app.route('/theorie/nomenklatur', methods=['GET'])
def nomenklatur():
    return render_template('/nomenklatur.html')


@app.route('/quellen', methods=['GET'])
def quellen():
    return render_template('/quellen.html')
