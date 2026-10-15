from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template("index.html", users=users)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/api/users", methods=["GET"])
def api_get_users():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify([{"id": u[0], "name": u[1], "email": u[2]} for u in users])

@app.route("/api/users", methods=["POST"])
def api_create_user():
    data = request.json
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (data["name"], data["email"]))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": user_id, "name": data["name"], "email": data["email"]}), 201

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return "", 204

if __name__ == "__main__":
    init_db()
    app.run(debug=True)