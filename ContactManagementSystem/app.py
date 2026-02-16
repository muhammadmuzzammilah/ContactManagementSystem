from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey123"   # required for login session

def db_connect():
    return sqlite3.connect("contacts.db")

# LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # developer credentials
        if username == "Muzz" and password == "Muzz&hii":
            session["logged_in"] = True
            return redirect("/contacts")
        else:
            return render_template("login.html", error="Invalid Login")

    return render_template("login.html")

# CONTACT PAGE (PROTECTED)
@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if not session.get("logged_in"):
        return redirect("/")

    conn = db_connect()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]

        cur.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email)
        )
        conn.commit()

    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    conn.close()

    return render_template("index.html", contacts=data)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)