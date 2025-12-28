from flask import Flask, render_template, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

def db_connection():
    return sqlite3.connect("incidents.db")

def create_table():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

create_table()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return {"status": "UP"}

@app.route("/simulate_failure")
def simulate_failure():
    conn = db_connection()
    cursor = conn.cursor()
    issues = [
        "Application Down",
        "Slow Response",
        "Database Connection Error",
        "API Timeout"
    ]

    issue = random.choice(issues)
    cursor.execute(
        "INSERT INTO incidents (issue, priority, status) VALUES (?, ?, ?)",
        (issue, "P1", "Open")
    )

    conn.commit()
    conn.close()
    return redirect(url_for("incidents"))

@app.route("/incidents")
def incidents():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template("incidents.html", incidents=data)

@app.route("/resolve/<int:id>")
def resolve(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE incidents SET status = ? WHERE id = ?",
        ("Resolved", id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("incidents"))

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
