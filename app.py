from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, comment TEXT)")
    conn.commit()
    conn.close()

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

