# Backend: Flask Server (app.py)
from flask import Flask, request, jsonify
import sqlite3
import bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, comment TEXT)")
    conn.commit()
    conn.close()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        response = {"message": "User registered successfully!"}
    except sqlite3.IntegrityError:
        response = {"error": "Username already exists!"}
    conn.close()
    return jsonify(response)

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"error": "Invalid username or password!"})

@app.route('/comments', methods=['GET'])
def get_comments():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT comment FROM comments")
    comments = c.fetchall()
    conn.close()
    return jsonify([comment[0] for comment in comments])

@app.route('/comment', methods=['POST'])
def post_comment():
    data = request.get_json()
    comment = data.get('comment')
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO comments (comment) VALUES (?)", (comment,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Comment added!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
