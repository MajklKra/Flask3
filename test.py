from flask import Flask, render_template, request, url_for, redirect
import mysql.connector

MyName = "Michal"
MyPassword = "Ostrava"

# Vytvoření instance Flask aplikace
app = Flask(__name__)

# Konfigurace připojení k MySQL databázi
db_config = {
    'host': '172.30.0.10',         # Název nebo IP adresa serveru
    'user': 'CODACOUSER',          # Uživatelské jméno MySQL
    'password': 'trasq774JUMP',    # Heslo k databázi
    'database': 'CodacoG2',        # Název databáze
    'port': 3306                   # Port (standardně 3306)
}


@app.route("/form")

def form():
    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Jednoduchá kontrola přihlašovacích údajů
        if username == MyName and password == MyPassword:
            #return render_template("index.html", devices)  # Přesměrování na stránku po přihlášení
            return redirect(url_for('device'))
        else:
            return render_template("login.html", error="Nesprávné přihlašovací údaje")  # Chyba přihlášení

    return render_template("login.html")  # Zobrazí přihlašovací formulář


@app.route("/")
def index():    
    #return redirect(url_for('login'))
    return render_template("index.html")
    

@app.route("/device")
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

        # Předání dat do šablony
        return render_template("device.html", devices=results)

    except mysql.connector.Error as err:
        # Zpracování chyby připojení
        return f"Chyba připojení k databázi: {err}"
    

@app.route("/device2")
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