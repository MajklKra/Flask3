import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask import abort
from functools import wraps
import secrets
from datetime import timedelta
from flask import session
from datetime import datetime

import locale

from babel.dates import format_datetime

# MyName = "Michal"
# MyPassword = "Ostrava"

# Vytvoření instance Flask aplikace
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Databáze uživatelů (pro jednoduchost hardcoded, použijte databázi pro produkci)
users = {
    "admin": {"password": bcrypt.generate_password_hash("adminpass").decode('utf-8'), "role": "admin"},
    "user": {"password": bcrypt.generate_password_hash("userpass").decode('utf-8'), "role": "user"},
    "footballer": {"password": bcrypt.generate_password_hash("fpass").decode('utf-8'), "role": "footballer"},
    "Michal": {"password": bcrypt.generate_password_hash("Ostrava").decode('utf-8'), "role": "author"},
}

# Konfigurace připojení k MySQL databázi
db_config = {
    'host': '172.30.0.10',         # Název nebo IP adresa serveru
    'user': 'CODACOUSER',          # Uživatelské jméno MySQL
    'password': 'trasq774JUMP',    # Heslo k databázi
    'database': 'CodacoG2',        # Název databáze
    'port': 3306                   # Port (standardně 3306)
}


# Třída User
class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role

# Načítání uživatele
@login_manager.user_loader
def load_user(username):
    user = users.get(username)
    if user:
        return User(username, user["role"])
    return None


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)  # Forbidden
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route("/")
def index():    
    #return redirect(url_for('login'))
    return render_template("index.html")
    #return "Domovská stránka. <a href='/login'>Přihlásit se</a>"

@app.route("/form")

def form():
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Odhlášení úspěšné!", "success")
    return redirect(url_for('login'))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = users.get(username)

        if user and bcrypt.check_password_hash(user['password'], password):
                # session['user'] = user
                login_user(User(username, user["role"]))
                flash("Přihlášení úspěšné!", "success")
                return redirect(url_for('device'))
        else:
            flash("Nesprávné uživatelské jméno nebo heslo !!!", "error")

    return render_template('login.html')

@app.route("/device")
@role_required('admin','user')
def device():
    try:
        # Připojení k MySQL databázi
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Provedení SQL dotazu
        query = "SELECT MacAddressStr,IPAddressStr, LastActivity, RunTime, VersionString FROM HwIpDevicesAddrMem;"

        query2 = """
                 SELECT DeviceTypeShortCut, MacAddressStr, IPAddressStr, LastActivity, RunTime, VersionString
                 FROM   HwIpDevicesAddrMem
                 JOIN   HwIpDevicesTypes ON HwIpDevicesTypes.DeviceTypeID = HwIpDevicesAddrMem.DeviceTypeID;
                 """
        
        query3 = """
                 SELECT *
                 FROM   HwIpDevicesTypes;
                 """

        cursor.execute(query2)
        results = cursor.fetchall()

        # Zavření kurzoru a připojení
        cursor.close()
        conn.close()

        current_time = datetime.now()
        formatted_time = format_datetime(current_time, "EEEE d. MMMM yyyy", locale="cs")
        formatted_time = formatted_time[0].upper() + formatted_time[1:]

        # Předání dat do šablony
        return render_template("device.html", devices=results, user=current_user, current_time=current_time, formatted_time=formatted_time)

    except mysql.connector.Error as err:
        # Zpracování chyby připojení
        return f"Chyba připojení k databázi: {err}"
    

@app.route("/device2")
@role_required('admin','user')
def device2():
    try:
        # Připojení k MySQL databázi
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Provedení SQL dotazu
        query = "SELECT MacAddressStr,IPAddressStr, LastActivity, RunTime, VersionString FROM HwIpDevicesAddrMem;"

        query2 = """
                 SELECT DeviceTypeShortCut, MacAddressStr, IPAddressStr, LastActivity, RunTime, VersionString
                 FROM   HwIpDevicesAddrMem
                 JOIN   HwIpDevicesTypes ON HwIpDevicesTypes.DeviceTypeID = HwIpDevicesAddrMem.DeviceTypeID;
                 """
        
        query3 = """
                 SELECT *
                 FROM   HwIpDevicesTypes;
                 """

        cursor.execute(query2)
        results = cursor.fetchall()

        # Zavření kurzoru a připojení
        cursor.close()
        conn.close()

        # Předání dat do šablony
        return render_template("device2.html", devices=results)

    except mysql.connector.Error as err:
        # Zpracování chyby připojení
        return f"Chyba připojení k databázi: {err}"



# Spuštění Flask serveru
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)