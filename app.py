from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Database connection
def get_db():
    return sqlite3.connect("database.db")

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM voters WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()

        if user:
            session["user"] = username
            return redirect("/vote")
        else:
            return "Invalid Login!"

    return render_template("login.html")


# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO voters (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        db.close()

        return redirect("/")

    return render_template("register.html")


# Vote Page
@app.route("/vote", methods=["GET", "POST"])
def vote():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        candidate = request.form.get("candidate")

        db = get_db()
        cur = db.cursor()
        cur.execute("UPDATE candidates SET votes = votes + 1 WHERE name=?", (candidate,))
        db.commit()
        db.close()

        return redirect("/result")

    return render_template("vote.html")


# Result Page
@app.route("/result")
def result():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM candidates")
    data = cur.fetchall()
    db.close()

    return render_template("result.html", data=data)


# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)