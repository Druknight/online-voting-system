import os
import sqlite3
import secrets
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-only-change-this-secret")
app.permanent_session_lifetime = timedelta(days=30)
DB_PATH = os.environ.get("DATABASE_PATH", "votes.db")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)
CANDIDATES = ["Angeline", "Sifuna", "Lenah", "Fidel"]

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            browser_token TEXT UNIQUE NOT NULL,
            candidate TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        candidate = request.form.get("candidate", "")
        if candidate not in CANDIDATES:
            flash("Please select one of the four candidates.")
            return redirect(url_for("index"))
        if session.get("has_voted"):
            flash("A vote has already been submitted from this browser.")
            return redirect(url_for("index"))
        browser_token = session.get("browser_token")
        if not browser_token:
            browser_token = secrets.token_urlsafe(32)
            session["browser_token"] = browser_token
        try:
            with connect() as db:
                db.execute("INSERT INTO votes (browser_token, candidate) VALUES (?, ?)",
                           (browser_token, candidate))
            session.permanent = True
            session["has_voted"] = True
            return render_template("thanks.html", candidate=candidate)
        except sqlite3.IntegrityError:
            session["has_voted"] = True
            flash("A vote has already been submitted from this browser.")
            return redirect(url_for("index"))
    return render_template("index.html", candidates=CANDIDATES)

@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        password = request.form.get("password", "")
        if not check_password_hash(ADMIN_PASSWORD_HASH, password):
            flash("Incorrect administrator password.")
            return redirect(url_for("results"))
        session["admin_ok"] = True
        return redirect(url_for("results"))
    if not session.get("admin_ok"):
        return render_template("login.html")
    with connect() as db:
        rows = db.execute("SELECT candidate, COUNT(*) AS total FROM votes GROUP BY candidate").fetchall()
        totals = {name: 0 for name in CANDIDATES}
        for row in rows:
            totals[row["candidate"]] = row["total"]
        total_votes = sum(totals.values())
    return render_template("results.html", totals=totals, total_votes=total_votes)

@app.route("/logout")
def logout():
    session.pop("admin_ok", None)
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
