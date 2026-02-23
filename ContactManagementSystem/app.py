from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "Muzz"



def db_connect():
    conn = sqlite3.connect("contacts.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT
        )
    """)
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
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

    conn.close()
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "muzz" and password == "hiii":
            session["admin"] = True
            return redirect("/admin")
        else:
            return "Invalid Login"

    return render_template("login.html")



@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    contacts = cur.fetchall()
    conn.close()

    return render_template("admin.html", contacts=contacts)



@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect("/login")

    conn = db_connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")



@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
